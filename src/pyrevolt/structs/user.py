from __future__ import annotations
from enum import Enum
import json
from ..client import HTTPClient, Request, Method
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..session import Session

class Relationship(Enum):
    Blocked = "Blocked"
    BlockedOther = "BlockedOther"
    Friend = "Friend"
    Incoming = "Incoming"
    Outgoing = "Outgoing"
    NoRelationship = "None"
    User = "User"

class Presence(Enum):
    Busy = "Busy"
    Idle = "Idle"
    Invisible = "Invisible"
    Online = "Online"

class Status:
    def __init__(self, presence: Presence, **kwargs) -> None:
        self.presence: Presence = presence
        self.text: str|None = kwargs.get("text")

    def __repr__(self) -> str:
        return f"<pyrevolt.Status presence={self.presence.value} text={self.text}>"

    @staticmethod
    async def FromJSON(jsonData: str|bytes) -> Status:
        data: dict = json.loads(jsonData)
        kwargs: dict = {}
        if data.get("text") is not None:
            kwargs["text"] = data["text"]
        return Status(Presence(data["presence"]), **kwargs)

class BotUser:
    def __init__(self, ownerID: str) -> None:
        self.ownerID: str = ownerID
    
    def __repr__(self) -> str:
        return f"<pyrevolt.Bot owner={self.ownerID}>"

class User:
    def __init__(self, userID: str, username: str, **kwargs) -> None:
        self.userID: str = userID
        self.username: str = username
        self.badges: int|None = kwargs.get("badges")
        self.online: bool|None = kwargs.get("online")
        self.relationship: Relationship|None = kwargs.get("relationship")
        self.status: dict|None = kwargs.get("status")
        self.flags: int|None = kwargs.get("flags")
        self.bot: BotUser|None = kwargs.get("bot")

    def __repr__(self) -> str:
        return f"<pyrevolt.User id={self.userID} username={self.username} badges={self.badges} relationship={self.relationship} online={self.online} bot={self.bot}>"

    async def update(self, updateData: dict) -> None:
        self.username = updateData.get("username", self.username)
        self.badges = updateData.get("badges", self.badges)
        self.online = updateData.get("online", self.online)
        if updateData.get("relationship") is not None:
            self.relationship = Relationship(updateData.get("relationship"))
        if updateData.get("status") is not None:
            self.status = await Status.FromJSON(json.dumps(updateData.get("status")))
        self.flags = updateData.get("flags", self.flags)
        self.bot = updateData.get("bot", self.bot)

    @property
    def mention(self) -> str:
        return f"<@{self.userID}>"

    @staticmethod
    async def FromJSON(jsonData: str|bytes, session: Session) -> User:
        data: dict = json.loads(jsonData)
        kwargs: dict = {}
        if data.get("badges") is not None:
            kwargs["badges"] = data["badges"]
        if data.get("online") is not None:
            kwargs["online"] = data["online"]
        if data.get("relationship") is not None:
            kwargs["relationship"] = Relationship(data["relationship"])
        if data.get("status") is not None:
            kwargs["status"] = await Status.FromJSON(json.dumps(data["status"]))
        if data.get("bot") is not None:
            kwargs["bot"] = BotUser(data["bot"]["owner"])
        user: User = User(data["_id"], data["username"], **kwargs)
        session.users[user.userID] = user
        return user
        
    @staticmethod
    async def FromID(userID: str, session) -> User:
        if session.users.get(userID) is not None:
            return session.users[userID]
        client: HTTPClient = HTTPClient()
        request: Request = Request(Method.GET, "/users/" + userID)
        request.AddAuthentication(session.token)
        result: dict = await client.Request(request)
        await client.Close()
        return await User.FromJSON(json.dumps(result), session)

    @staticmethod
    async def AttemptParse(content: str, session: Session) -> User | bool:
        if content.startswith("<@") and content.endswith(">"):
            userID: str = content[2:content.find(">")]
            user: User | None = session.users.get(userID)
            if user is None:
                user = await User.FromID(userID, session)
            return user
        return False