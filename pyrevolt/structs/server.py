from __future__ import annotations
import json
from ..client import Method
from ..structs.channels import ServerChannel, Channel
from ..structs.user import User
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..session import Session
    from .member import Member
    from .channels import ChannelType

class Category:
    def __init__(self, categoryID: str, title: str, channels: list[ServerChannel]) -> None:
        self.categoryID: str = categoryID
        self.title: str = title
        self.channels: list[ServerChannel] = channels

    def __repr__(self) -> str:
        return f"<pyrevolt.Category id={self.categoryID} title={self.title} channels={self.channels}>"

    @staticmethod
    async def FromJSON(jsonData: str|bytes, session: Session) -> Category:
        data: dict = json.loads(jsonData)
        channels: list[ServerChannel] = []
        for channel in data["channels"]:
            channel: ServerChannel|None = await ServerChannel.FromID(channel, session)
            if channel is not None:
                channels.append(channel)
            
        return Category(data["id"], data["title"], channels)

class SystemMessages:
    def __init__(self, **kwargs) -> None:
        self.userJoinedChannel: ServerChannel|None = kwargs.get("userJoinedChannel")
        self.userLeftChannel: ServerChannel|None = kwargs.get("userLeftChannel")
        self.userKickedChannel: ServerChannel|None = kwargs.get("userKickedChannel")
        self.userBannedChannel: ServerChannel|None = kwargs.get("userBannedChannel")

    def __repr__(self) -> str:
        return f"<pyrevolt.SystemMessages userJoinedChannel={self.userJoinedChannel} userLeftChannel={self.userLeftChannel} userKickedChannel={self.userKickedChannel} userBannedChannel={self.userBannedChannel}>"

    @staticmethod
    async def FromJSON(jsonData: str|bytes, session: Session) -> SystemMessages:
        data: dict = json.loads(jsonData)
        kwargs: dict = {}
        if data.get("userJoinedChannel") is not None:
            kwargs["userJoinedChannel"] = await ServerChannel.FromJSON(json.dumps(data["userJoinedChannel"]), session)
        if data.get("userLeftChannel") is not None:
            kwargs["userLeftChannel"] = await ServerChannel.FromJSON(json.dumps(data["userLeftChannel"]), session)
        if data.get("userKickedChannel") is not None:
            kwargs["userKickedChannel"] = await ServerChannel.FromJSON(json.dumps(data["userKickedChannel"]), session)
        if data.get("userBannedChannel") is not None:
            kwargs["userBannedChannel"] = await ServerChannel.FromJSON(json.dumps(data["userBannedChannel"]), session)
        return SystemMessages(**kwargs)

class Role:
    def __init__(self, roleID: str, name: str, permissions, **kwargs) -> None:
        self.roleID: str = roleID
        self.name: str = name
        self.permissions = permissions
        self.colour: int|None = kwargs.get("colour")
        self.hoist: bool|None = kwargs.get("hoist")
        self.rank: int|None = kwargs.get("rank")

    def __repr__(self) -> str:
        return f"<pyrevolt.Roles name={self.name} permissions={self.permissions} colour={self.colour} hoist={self.hoist} rank={self.rank}>"

    async def update(self, updatedData: dict, clear: list[str] = []) -> None:
        for key, value in updatedData.items():
            setattr(self, key, value)
        for key in clear:
            setattr(self, key, None)

    @staticmethod
    async def FromJSON(jsonData: str|bytes) -> Role:
        data: dict = json.loads(jsonData)
        kwargs: dict = {}
        if data.get("colour") is not None:
            kwargs["colour"] = data["colour"]
        if data.get("hoist") is not None:
            kwargs["hoist"] = data["hoist"]
        if data.get("rank") is not None:
            kwargs["rank"] = data["rank"]
        return Role(data["_id"], data["name"], data["permissions"], **kwargs)

class Server:
    def __init__(self, serverID: str, owner: User, name: str, channels: list[ServerChannel], defaultPermissions, **kwargs) -> None:
        self.serverID: str = serverID
        self.owner: User = owner
        self.name: str = name
        self.channels: list[ServerChannel] = channels
        self.defaultPermissions = defaultPermissions
        self.description: str|None = kwargs.get("description")
        self.categories: Category|None = kwargs.get("categories")
        self.systemMessages: SystemMessages|None = kwargs.get("systemMessages")
        self.roles: dict[str, Role]|None = kwargs.get("roles")
        self.nsfw: bool|None = kwargs.get("nsfw")
        self.flags: int|None = kwargs.get("flags")
        self.analytics: bool|None = kwargs.get("analytics")
        self.discoverable: bool|None = kwargs.get("discoverable")
        self.session: Session|None = kwargs.get("session")

    def __repr__(self) -> str:
        return f"<pyrevolt.Server id={self.serverID} owner={self.owner} name={self.name} channels={self.channels} defaultPermissions={self.defaultPermissions}>"
    
    def copy(self) -> Server:
        return Server(self.serverID, self.owner, self.name, self.channels, self.defaultPermissions, categories=self.categories, systemMessages=self.systemMessages, roles=self.roles, nsfw=self.nsfw, flags=self.flags, analytics=self.analytics, discoverable=self.discoverable)

    async def update(self, updatedData: dict, clear: list[str] = [], **kwargs) -> None:
        if updatedData.get("owner") is not None:
            self.owner = await User.FromID(updatedData["owner"], kwargs["session"])
        if updatedData.get("name") is not None:
            self.name = updatedData["name"]
        if updatedData.get("description") is not None:
            self.description = updatedData["description"]
        if updatedData.get("channels") is not None:
            self.channels = []
            for channel in updatedData["channels"]:
                channel: ServerChannel|None = await kwargs["session"].GetChannel(channel)
                if channel is not None:
                    self.channels.append(channel)
        if updatedData.get("default_permissions") is not None:
            self.defaultPermissions = updatedData["default_permissions"]
        if updatedData.get("categories") is not None:
            self.categories = []
            for category in updatedData["categories"]:
                category: Category|None = await Category.FromJSON(json.dumps(category), kwargs["session"])
                if category is not None:
                    self.categories.append(category)
        if updatedData.get("systemMessages") is not None:
            self.systemMessages = SystemMessages.FromJSON(json.dumps(updatedData["systemMessages"]), kwargs["session"])
        if updatedData.get("roles") is not None:
            self.roles = {}
            for role in updatedData["roles"]:
                role: Role|None = await Role.FromJSON(json.dumps(role))
                if role is not None:
                    self.roles[role.roleID] = role
        if updatedData.get("nsfw") is not None:
            self.nsfw = updatedData["nsfw"]
        if updatedData.get("flags") is not None:
            self.flags = updatedData["flags"]
        if updatedData.get("analytics") is not None:
            self.analytics = updatedData["analytics"]
        if updatedData.get("discoverable") is not None:
            self.discoverable = updatedData["discoverable"]

        for key in clear:
            setattr(self, key, None)

    @staticmethod
    async def FromJSON(jsonData: str|bytes, session: Session) -> Server:
        data: dict = json.loads(jsonData)
        kwargs: dict = {}
        kwargs["session"] = session

        if data.get("description") is not None:
            kwargs["description"] = data["description"]
        if data.get("roles") is not None:
            roles: dict[str, Role] = {}
            for roleID, role in data["roles"].items():
                role["_id"] = roleID
                roles[roleID] = await Role.FromJSON(json.dumps(role))
            kwargs["roles"] = roles
        if data.get("nsfw") is not None:
            kwargs["nsfw"] = data["nsfw"]
        if data.get("flags") is not None:
            kwargs["flags"] = data["flags"]
        if data.get("analytics") is not None:
            kwargs["analytics"] = data["analytics"]
        if data.get("discoverable") is not None:
            kwargs["discoverable"] = data["discoverable"]

        server: Server = Server(data["_id"], await User.FromID(data["owner"], session), data["name"], [], data["default_permissions"], **kwargs)
        session.servers[server.serverID] = server
        channels: list[ServerChannel] = []
        for channel in data["channels"]:
            channels.append(await ServerChannel.FromID(channel, session))
        server.channels = channels
        if data.get("categories") is not None:
            categories: list[Category] = []
            for category in data["categories"]:
                categories.append(await Category.FromJSON(json.dumps(category), session))
            server.categories = categories
        if data.get("systemMessages") is not None:
            server.systemMessages = await SystemMessages.FromJSON(json.dumps(data["systemMessages"]), session)
        return server

    @staticmethod
    async def FromID(serverID: str, session: Session) -> Server:
        if session.servers.get(serverID) is not None:
            return session.servers[serverID]
        result: dict = await session.Request(Method.GET, f"/servers/{serverID}")
        if result.get("type") is not None:
            return
        return await Server.FromJSON(json.dumps(result), session)

    async def CreateChannel(self, name: str, **kwargs) -> Channel:
        data: dict = {"name": name}
        if kwargs.get("type") is not None:
            if kwargs["type"] == ChannelType.TextChannel:
                data["type"] = "Text"
            elif kwargs["type"] == ChannelType.VoiceChannel:
                data["type"] = "Voice"
        if kwargs.get("description") is not None:
            data["description"] = kwargs["description"]
        if kwargs.get("nsfw") is not None:
            data["nsfw"] = kwargs["nsfw"]
        
        result: dict = await self.session.Request(Method.POST, f"/servers/{self.serverID}/channels", data=data)
        return await Channel.FromJSON(json.dumps(result), self.session)

    async def Edit(self, **kwargs) -> None:
        data: dict = {}
        if kwargs.get("name") is not None:
            data["name"] = kwargs["name"]
        if kwargs.get("description") is not None:
            data["description"] = kwargs["description"]
        if kwargs.get("analytics") is not None:
            data["analytics"] = kwargs["analytics"]
        if kwargs.get("remove") is not None:
            data["remove"] = kwargs["remove"]

        result: dict = await self.session.Request(Method.PATCH, f"/servers/{self.serverID}", data=data)
        if result.get("type") is None:
            await self.update(result, data["remove"])

    async def Delete(self) -> None:
        await self.session.Request(Method.DELETE, f"/servers/{self.serverID}")
        self.session.servers.pop(self.serverID)

    async def Kick(self, member: Member) -> None:
        if member.server != self:
            raise ValueError("Member is not in this server")
        await self.session.Request(Method.DELETE, f"/servers/{self.serverID}/members/{member.userID}")

    async def Ban(self, member: Member) -> None:
        if member.server != self:
            raise ValueError("Member is not in this server")
        await self.session.Request(Method.PUT, f"/servers/{self.serverID}/bans/{member.userID}")

    async def Unban(self, user: User) -> None:
        await self.session.Request(Method.DELETE, f"/servers/{self.serverID}/bans/{user.userID}")