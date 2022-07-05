import json
from .exceptions import WebsocketError, InternalWebsocketError, InvalidSession, OnboardingNotFinished, AlreadyAuthenticated
from .client import HTTPClient, Method, Request
from .gateway import Gateway, GatewayEvent
from .structs.channels import Channel, Message
from .structs.user import Relationship, User
from .structs.server import Server, Role
from .structs.member import Member
from .structs.invite import Invite

class Session:
    def __init__(self) -> None:
        self.gateway: Gateway = Gateway()
        self.client: HTTPClient = HTTPClient()
        self.token: str|None = None
        self.users: dict[str, User] = {}
        self.channels: dict[str, Channel] = {}
        self.servers: dict[str, Server] = {}
        self.members: dict[str, Member] = {}
        self.messages: dict[str, Message] = {}

    async def Connect(self) -> None:
        await self.gateway.Connect()

    async def Start(self, token: str) -> None:
        await self.Connect()
        await self.gateway.Authenticate(token)
        self.token = token

        request: dict = await self.Request(Method.GET, "/users/@me")
        self.self: User = await self.GetUser(request["_id"])

    async def Close(self) -> None:
        await self.gateway.Close()
        await self.client.Close()
    
    async def Request(self, method: Method, url: str, **kwargs) -> dict:
        request: Request = Request(method, url, **kwargs)
        request.AddAuthentication(self.token)
        return await self.client.Request(request)

    async def ProcessGateway(self, data: dict) -> dict:
        for event in GatewayEvent:
            if data["type"] == event.value.VALUE:
                data["type"] = event.value
                break

        args: list = []
        kwargs: dict = {}

        match data["type"]:
            case GatewayEvent.Error.value:
                match data["error"]:
                    case "LabelMe":
                        raise WebsocketError("An error occured")
                    case "InternalError":
                        raise InternalWebsocketError("An internal error occured")
                    case "InvalidSession":
                        raise InvalidSession("The session is invalid")
                    case "OnboardingNotFinished":
                        raise OnboardingNotFinished("The onboarding is not finished")
                    case "AlreadyAuthenticated":
                        raise AlreadyAuthenticated("The session is already authenticated")
                    case _:
                        raise WebsocketError("An error occured")
            case GatewayEvent.Bulk.value:
                for event in data["v"]:
                    await self.ProcessGateway(event)
                return
            case GatewayEvent.Ready.value:
                await GatewayEvent.ReadySimplified.value.dispatch()
                for index, user in enumerate(data["users"]):
                    user: User = await User.FromJSON(json.dumps(user), self)
                    data["users"][index] = user
                for index, channel in enumerate(data["channels"]):
                    channel: Channel = await Channel.FromJSON(json.dumps(channel), self)
                    data["channels"][index] = channel
                for index, server in enumerate(data["servers"]):
                    server: Server = await Server.FromJSON(json.dumps(server), self)
                    data["servers"][index] = server
                for index, member in enumerate(data["members"]):
                    member: Member = await Member.FromJSON(json.dumps(member), self)
                    data["members"][index] = member
                args.append(data["users"])
                args.append(data["channels"])
                args.append(data["servers"])
                args.append(data["members"])
            case GatewayEvent.OnMessage.value:
                message: dict = data.copy()
                message.pop("type")
                message: Message = await Message.FromJSON(json.dumps(message), self)
                self.messages[message.messageID] = message
                args.append(message)
            case GatewayEvent.MessageUpdate.value:
                message: Message = self.messages.get(data["id"], await Message.FromID(data["channel"], data["id"], self)).copy()
                args.append(message)
                newMessage: Message = await Message.FromID(data["channel"], data["id"], self)
                await newMessage.update(data["data"])
                if newMessage.content == message.content:
                    return {"type": data["type"]}
                args.append(newMessage)
            case GatewayEvent.MessageDelete.value:
                message: Message = self.messages.get(data["id"])
                if message is None:
                    return {"type": data["type"]}
                self.messages.pop(data["id"])
                args.append(message)
            case GatewayEvent.ChannelCreate.value:
                channelData: dict = data.copy()
                channelData.pop("type")
                channel: Channel = await Channel.FromJSON(json.dumps(channelData), self)
                self.channels[channel.channelID] = channel
                args.append(channel)
            case GatewayEvent.ChannelUpdate.value:
                channel: Channel = self.channels.get(data["id"], await Channel.FromID(data["id"], self)).copy()
                args.append(channel)
                newChannel: Channel = await Channel.FromID(data["id"], self)
                await newChannel.update(data["data"], data.get("clear", []))
                args.append(newChannel)
            case GatewayEvent.ChannelDelete.value:
                channel: Channel = self.channels.get(data["id"])
                if channel is None:
                    return {"type": data["type"]}
                self.channels.pop(data["id"])
                args.append(channel)
            case GatewayEvent.ChannelGroupJoin.value | GatewayEvent.ChannelGroupLeave.value:
                channel: Channel = self.channels.get(data["id"], await Channel.FromID(data["id"], self))
                user: User = self.users.get(data["user"], await User.FromID(data["user"], self))
                if data["type"] == GatewayEvent.ChannelGroupJoin.value:
                    channel.users.append(user)
                else:
                    channel.users.remove(user)
                args.append(channel)
                args.append(user)
            case GatewayEvent.ChannelStartTyping.value | GatewayEvent.ChannelStopTyping.value:
                channel: Channel = self.channels.get(data["id"], await Channel.FromID(data["id"], self))
                user: User = self.users.get(data["user"], await User.FromID(data["user"], self))
                args.append(channel)
                args.append(user)
            case GatewayEvent.ChannelAck.value:
                # Could use this for possible implementation in the future
                pass
            case GatewayEvent.ServerCreate.value:
                server: Server = await Server.FromJSON(json.dumps(data), self)
                self.servers[server.serverID] = server
                args.append(server)
            case GatewayEvent.ServerUpdate.value:
                server: Server = self.servers.get(data["id"], await Server.FromID(data["id"], self)).copy()
                args.append(server)
                newServer: Server = await Server.FromID(data["id"], self)
                await newServer.update(data["data"], data.get("clear", []), session=self)
                args.append(newServer)
            case GatewayEvent.ServerDelete.value:
                server: Server = self.servers.get(data["id"])
                if server is None:
                    return {"type": data["type"]}
                self.servers.pop(data["id"])
                args.append(server)
            case GatewayEvent.ServerMemberUpdate.value:
                member: Member = await Member.FromID(data["id"]["server"] + "." + data["id"]["user"], self)
                args.append(member)
                newMember: Member = member.copy()
                await newMember.update(data["data"], data.get("clear", []))
                args.append(newMember)
            case GatewayEvent.ServerMemberJoin.value | GatewayEvent.ServerMemberLeave.value:
                member: Member = await Member.FromID(data["id"] + "." + data["user"], self)
                if data["type"] == GatewayEvent.ServerMemberJoin.value:
                    self.members[member.memberID] = member
                    if self.users.get(member.user.userID) is None:
                        self.users[member.user.userID] = member.user
                else:
                    self.members.pop(member.memberID)
                args.append(member)
            case GatewayEvent.ServerRoleUpdate.value:
                server: Server = self.servers.get(data["id"], await Server.FromID(data["id"], self))
                if server.roles.get(data["role_id"]) is None:
                    data["data"]["_id"] = data["role_id"]
                    server.roles[data["role_id"]] = await Role.FromJSON(json.dumps(data["data"]), self)
                else:
                    await server.roles[data["role_id"]].update(data["data"], data.get("clear", []))
                args.append(server)
                args.append(server.roles[data["role_id"]])
            case GatewayEvent.ServerRoleDelete.value:
                server: Server = self.servers.get(data["id"], await Server.FromID(data["id"], self))
                if server.roles.get(data["role_id"]) is None:
                    return {"type": data["type"]}
                args.append(server)
                args.append(server.roles[data["role_id"]])
                server.roles.pop(data["role_id"])
            case GatewayEvent.UserUpdate.value:
                user: User = self.users.get(data["id"], await User.FromID(data["id"], self)).copy()
                args.append(user)
                newUser: User = await User.FromID(data["id"], self)
                await newUser.update(data["data"], data.get("clear", []))
                args.append(newUser)
            case GatewayEvent.UserRelationship.value:
                user: User = self.users.get(data["user"], await User.FromID(data["user"], self))
                await user.update({"relationship": data["status"]})
                args.append(user)
                args.append(Relationship(data["status"]))
        
        await data["type"].dispatch(*args, **kwargs)
        return data

    async def GatewayReceive(self) -> dict:
        return await self.ProcessGateway(await self.gateway.Receive())

    async def GetUser(self, userID: str) -> User:
        if self.users.get(userID) is None:
            data: dict = await self.Request(Method.GET, f"/users/{userID}")
            user: User = await User.FromJSON(json.dumps(data), self)
            return user
        else:
            return self.users[userID]

    async def GetChannel(self, channelID: str) -> Channel:
        if self.channels.get(channelID) is None:
            data: dict = await self.Request(Method.GET, f"/channels/{channelID}")
            channel: Channel = await channel.FromJSON(json.dumps(data), self)
            return channel
        else:
            return self.channels[channelID]

    async def GetMessage(self, channelID: str, messageID: str) -> Message:
        if self.messages.get(messageID) is None:
            data: dict = await self.Request(Method.GET, f"/channels/{channelID}/messages/{messageID}")
            message: Message = await Message.FromJSON(json.dumps(data), self)
            return message
        else:
            return self.messages[messageID]

    async def GetServer(self, serverID: str) -> Server:
        if self.servers.get(serverID) is None:
            data: dict = await self.Request(Method.GET, f"/servers/{serverID}")
            server: Server = await Server.FromJSON(json.dumps(data), self)
            return server
        else:
            return self.servers[serverID]

    async def GetMember(self, serverID: str, userID: str) -> Member:
        if self.members.get(serverID + "." + userID) is None:
            data: dict = await self.Request(Method.GET, f"/servers/{serverID}/members/{userID}")
            member: Member = await Member.FromJSON(json.dumps(data), self)
            return member
        return self.members[serverID + "." + userID]

    async def GetRole(self, serverID: str, roleID: str) -> Role:
        server: Server = await self.GetServer(serverID)
        return server.roles.get(roleID)

    async def GetInvite(self, inviteID: str) -> Invite:
        return await Invite.FromJSON(json.dumps(await self.Request(Method.GET, f"/invites/{inviteID}")), self)
