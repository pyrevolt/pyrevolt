from __future__ import annotations
from enum import Enum
import json
from ..client import Method
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..session import Session

class InviteType(Enum):
    Server = "Server"
    Group = "Group"

class Invite:
    def __init__(self, inviteType: InviteType, code: str, channelID: str, channelName: str, username: str, **kwargs):
        self.inviteType: InviteType = inviteType
        self.code: str = code
        self.channelID: str = channelID
        self.channelName: str = channelName
        self.username: str = username
        self.channelDescription: str | None = kwargs.get("channelDescription")
        self.session: Session|None = kwargs.get("session")

    @staticmethod
    async def FromJSON(jsonData: str|bytes, session: Session) -> Invite:
        data: dict = json.loads(jsonData)
        kwargs: dict = {"session": session}

        if data.get("channel_description") is not None:
            kwargs["channelDescription"] = data["channel_description"]
        match data["type"]:
            case InviteType.Server.value:
                return ServerInvite(data["code"], data["channel_id"], data["channel_name"], data["user_name"], data["server_id"], data["server_name"], data["member_count"], **kwargs)
            case InviteType.Group.value:
                return GroupInvite(data["code"], data["channel_id"], data["channel_name"], data["user_name"], **kwargs)

    async def Delete(self) -> None:
        await self.session.Request(Method.DELETE, f"/invites/{self.code}")

class ServerInvite(Invite):
    def __init__(self, code: str, channelID: str, channelName: str, username: str, serverID: str, serverName: str, memberCount: int, **kwargs):
        self.memberCount: int = memberCount
        self.serverID: str = serverID
        self.serverName: str = serverName
        self.channelDescription: str|None = kwargs.get("channelDescription")
        super().__init__(InviteType.Server, code, channelID, channelName, username, **kwargs)

    def __repr__(self) -> str:
        return f"<pyrevolt.ServerInvite code={self.code} serverID={self.serverID} memberCount={self.memberCount} serverName={self.channelName} channelID={self.channelID} channelName={self.channelName} username={self.username}>"

class GroupInvite(Invite):
    def __init__(self, code: str, channelID: str, channelName: str, username: str, **kwargs):
        super().__init__(InviteType.Group, code, channelID, channelName, username, **kwargs)

    def __repr__(self) -> str:
        return f"<pyrevolt.GroupInvite code={self.code} channelID={self.channelID} channelName={self.channelName} username={self.username}>"