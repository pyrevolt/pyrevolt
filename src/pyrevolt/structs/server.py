from __future__ import annotations
import json
from ..structs.channels import ServerChannel
from ..structs.user import User
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..session import Session

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

    @staticmethod
    async def FromJSON(jsonData: str|bytes, session: Session) -> Role:
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
        self.categories: Category|None = kwargs.get("categories")
        self.systemMessages: SystemMessages|None = kwargs.get("systemMessages")
        self.roles: Role|None = kwargs.get("roles")
        self.nsfw: bool|None = kwargs.get("nsfw")
        self.flags: int|None = kwargs.get("flags")
        self.analytics: bool|None = kwargs.get("analytics")
        self.discoverable: bool|None = kwargs.get("discoverable")

    def __repr__(self) -> str:
        return f"<pyrevolt.Server id={self.serverID} owner={self.owner} name={self.name} channels={self.channels} defaultPermissions={self.defaultPermissions} categories={self.categories} systemMessages={self.systemMessages} roles={self.roles} nsfw={self.nsfw} flags={self.flags} analytics={self.analytics} discoverable={self.discoverable}>"
    
    @staticmethod
    async def FromJSON(jsonData: str|bytes, session: Session) -> Server:
        data: dict = json.loads(jsonData)
        kwargs: dict = {}
        channels: list[ServerChannel] = []
        for channel in data["channels"]:
            channels.append(await ServerChannel.FromID(channel, session))

        if data.get("categories") is not None:
            categories: list[Category] = []
            for category in data["categories"]:
                categories.append(await Category.FromJSON(json.dumps(category), session))
            kwargs["categories"] = categories
        if data.get("systemMessages") is not None:
            kwargs["systemMessages"] = await SystemMessages.FromJSON(json.dumps(data["systemMessages"]), session)
        if data.get("roles") is not None:
            roles: list[Role] = []
            for roleID, role in data["roles"].items():
                role["_id"] = roleID
                roles.append(await Role.FromJSON(json.dumps(role), session))
            kwargs["roles"] = roles
        if data.get("nsfw") is not None:
            kwargs["nsfw"] = data["nsfw"]
        if data.get("flags") is not None:
            kwargs["flags"] = data["flags"]
        if data.get("analytics") is not None:
            kwargs["analytics"] = data["analytics"]
        if data.get("discoverable") is not None:
            kwargs["discoverable"] = data["discoverable"]

        server: Server = Server(data["_id"], await User.FromID(data["owner"], session), data["name"], channels, data["default_permissions"], **kwargs)
        session.servers[server.serverID] = server
        return server