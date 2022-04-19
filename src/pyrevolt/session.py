import json
from .client import HTTPClient, Method, Request
from .gateway import Gateway, GatewayEvent
from .structs.channels import Channel, Message
from .structs.user import User
from .structs.server import Server

class Session:
    def __init__(self) -> None:
        self.gateway: Gateway = Gateway()
        self.client: HTTPClient = HTTPClient()
        self.token: str|None = None
        self.users: dict[str, User] = {}
        self.channels: dict[str, Channel] = {}
        self.servers: dict[str, Server] = {}

    async def Connect(self) -> None:
        await self.gateway.Connect()

    async def Start(self, token: str) -> None:
        await self.Connect()
        await self.gateway.Authenticate(token)
        self.token = token

    async def Close(self) -> None:
        await self.gateway.Close()
        await self.client.Close()
    
    async def Request(self, method: Method, url: str, **kwargs) -> dict:
        request: Request = Request(method, url, **kwargs)
        request.AddAuthentication(self.token)
        return await self.client.Request(request)

    async def GatewayReceive(self) -> dict:
        data: dict = await self.gateway.Receive()
        for event in GatewayEvent:
            if data["type"] == event.value.VALUE:
                data["type"] = event.value
                break

        args: dict = []
        kwargs: dict = {}

        match data["type"]:
            case GatewayEvent.Ready.value:
                for index, user in enumerate(data["users"]):
                    user: User = await User.FromJSON(json.dumps(user), self)
                    data["users"][index] = user
                    self.users[user.userID] = user
                for index, channel in enumerate(data["channels"]):
                    channel: Channel = await Channel.FromJSON(json.dumps(channel), self)
                    data["channels"][index] = channel
                    self.channels[channel.channelID] = channel
                for index, server in enumerate(data["servers"]):
                    server: Server = await Server.FromJSON(json.dumps(server), self)
                    data["servers"][index] = server
                    self.servers[server.serverID] = server
                kwargs["users"] = data["users"]
                kwargs["channels"] = data["channels"]
                kwargs["servers"] = data["servers"]
            case GatewayEvent.UserUpdate.value:
                user: User | None = self.users.get(data["id"])
                if user is not None:
                    await user.Update(data["data"])
                    args.append(user)
            case GatewayEvent.Message.value:
                kwargs["message"] = await Message.FromJSON(data, self)
                    
        await data["type"].dispatch(*args, **kwargs)
        return data