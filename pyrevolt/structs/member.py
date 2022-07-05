from __future__ import annotations
import json
from typing import TYPE_CHECKING
from ..client import Method
if TYPE_CHECKING:
    from .user import User
    from .server import Server, Role
    from ..session import Session

class Member:
    def __init__(self, user: User, server: Server, **kwargs) -> None:
        self.user: User = user
        self.server: Server = server
        self.nickname: str|None = kwargs.get("nickname")
        self.roles: list[Role]|None = kwargs.get("roles")

    def __repr__(self) -> str:
        return f"<pyrevolt.Member id={self.memberID} user={self.user} server={self.server} nickname={self.nickname} roles={self.roles}>"

    def __str__(self) -> str:
        return self.user.username

    @property
    def memberID(self) -> str:
        return self.server.serverID + "." + self.user.userID

    def copy(self) -> Member:
        return Member(self.user, self.server, nickname=self.nickname, roles=self.roles)

    async def update(self, data: dict, clear: list[str] = []) -> None:
        if data.get("nickname") is not None:
            self.nickname = data["nickname"]
        if data.get("roles") is not None:
            roles: list[Role] = []
            for roleID in data["roles"]:
                role = self.server.roles.get(roleID)
                if role is not None:
                    roles.append(role)
            self.roles = roles
        for key in clear:
            setattr(self, key, None)

    @staticmethod
    async def FromJSON(jsonData: str|bytes, session: Session) -> Member:
        data: dict = json.loads(jsonData)
        kwargs: dict = {}
        if data.get("nickname") is not None:
            kwargs["nickname"] = data["nickname"]
        if data.get("roles") is not None:
            kwargs["roles"] = []
            for roleID in data["roles"]:
                kwargs["roles"].append(await session.GetRole(data["_id"]["server"], roleID))
        member: Member = Member(await session.GetUser(data["_id"]["user"]), await session.GetServer(data["_id"]["server"]), **kwargs)
        session.members[member.server.serverID + "." + member.user.userID] = member
        return member

    @staticmethod
    async def FromID(memberID: str, session: Session) -> Member:
        if session.members.get(memberID) is not None:
            return session.members[memberID]
        ids: list[str] = memberID.split(".")
        result: dict = await session.Request(Method.GET, f"/servers/{ids[0]}/members/{ids[1]}")
        if result.get("type") is not None:
            return
        return await Member.FromJSON(json.dumps(result), session)

    async def Kick(self) -> None:
        await self.server.Kick(self)

    async def Ban(self) -> None:
        await self.server.Ban(self)

    async def Unban(self) -> None:
        await self.server.Unban(self)

    async def Edit(self, **kwargs) -> None:
        data: dict = {}
        if kwargs.get("nickname") is not None:
            data["nickname"] = kwargs["nickname"]
        if kwargs.get("roles") is not None:
            data["roles"] = []
            for role in kwargs["roles"]:
                data["roles"].append(role.roleID)
        if kwargs.get("remove") is not None:
            data["remove"] = kwargs["remove"]

        result: dict = await self.server.session.Request(Method.PATCH, f"/servers/{self.server.serverID}/members/{self.user.userID}", data=data)
        await self.update(result)