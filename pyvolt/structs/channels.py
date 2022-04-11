from __future__ import annotations
from enum import Enum
import json
from typing import List
from .user import User

class ChannelType(Enum):
    SavedMessages = "SavedMessages"
    DirectMessage = "DirectMessage"
    Group = "Group"
    TextChannel = "TextChannel"
    VoiceChannel = "VoiceChannel"

class Channel:
    def __init__(self, channelID: str, type: ChannelType) -> None:
        self.channelID: str = channelID
        self.type: ChannelType = type

    def __repr__(self) -> str:
        return f"<pyvolt.{self.type.value} id={self.channelID}>"

    @staticmethod
    async def FromJSON(jsonData: str|bytes, session) -> Channel:
        data: dict = json.loads(jsonData)
        kwargs: dict = {}
        match data["channel_type"]:
            case ChannelType.SavedMessages.value:
                user: User|None = session.users.get(data["user"])
                if user is None:
                    user = await User.FromID(data["user"], session.token)
                return SavedMessages(data["_id"], user)
            case ChannelType.DirectMessage.value:
                if data.get("last_message_id") is not None:
                    kwargs["lastMessageID"] = data["last_message_id"]
                recipients: List[User] = []
                for userID in data["recipients"]:
                    user: User|None = session.users.get(userID)
                    if user is None:
                        user = await User.FromID(userID, session.token)
                    recipients.append(user)
                return DirectMessage(data["_id"], data["active"], recipients, **kwargs)
            case ChannelType.Group.value:
                if data.get("description") is not None:
                    kwargs["description"] = data["description"]
                if data.get("last_message_id") is not None:
                    kwargs["lastMessageID"] = data["last_message_id"]
                if data.get("permissions") is not None:
                    kwargs["permissions"] = data["permissions"]
                if data.get("nsfw") is not None:
                    kwargs["nsfw"] = data["nsfw"]
                recipients: List[User] = []
                owner: User = None
                for userID in data["recipients"]:
                    user: User|None = session.users.get(userID)
                    if user is None:
                        user = await User.FromID(userID, session.token)
                    if user.userID == data["owner"]:
                        owner = user
                    recipients.append(user)
                return Group(data["_id"], data["name"], recipients, owner, **kwargs)
            case ChannelType.TextChannel.value:
                if data.get("description") is not None:
                    kwargs["description"] = data["description"]
                if data.get("default_permissions") is not None:
                    kwargs["defaultPermissions"] = data["defaultPermissions"]
                if data.get("nsfw") is not None:
                    kwargs["nsfw"] = data["nsfw"]
                if data.get("last_message_id") is not None:
                    kwargs["lastMessageID"] = data["last_message_id"]
                return TextChannel(data["_id"], data["server"], data["name"], **kwargs)
            case ChannelType.VoiceChannel.value:
                if data.get("description") is not None:
                    kwargs["description"] = data["description"]
                if data.get("default_permissions") is not None:
                    kwargs["defaultPermissions"] = data["defaultPermissions"]
                if data.get("nsfw") is not None:
                    kwargs["nsfw"] = data["nsfw"]
                return VoiceChannel(data["_id"], data["server"], data["name"], **kwargs)

class SavedMessages(Channel):
    def __init__(self, channelID: str, user: User) -> None:
        self.user: User = user
        super().__init__(channelID, ChannelType.SavedMessages)

class DirectMessage(Channel):
    def __init__(self, channelID: str, active: bool, recipients: List[User], **kwargs) -> None:
        self.active: bool = active
        self.recipients: List[User] = recipients
        self.lastMessageID: str|None = kwargs.get("lastMessageID")
        super().__init__(channelID, ChannelType.DirectMessage)

class Group(Channel):
    def __init__(self, channelID: str, name: str, recipients: List[User], owner: User, **kwargs) -> None:
        self.name: str = name
        self.recipients: List[User] = recipients
        self.owner: User = owner
        self.description: str|None = kwargs.get("description")
        self.lastMessageID: str|None = kwargs.get("lastMessageID")
        # TODO: Icon
        self.permissions: int|None = kwargs.get("permissions")
        self.nsfw: bool|None = kwargs.get("nsfw")
        super().__init__(channelID, ChannelType.Group)

class ServerChannel(Channel):
    def __init__(self, channelID: str, type: ChannelType, server, name: str, **kwargs) -> None:
        self.server = server
        self.name: str = name
        self.description: str | None = kwargs.get("description")
        # TODO: Icon
        self.defaultPermissions: int | None = kwargs.get("defaultPermissions")
        # TODO: Role permissions
        self.nsfw: bool | None = kwargs.get("nsfw")
        super().__init__(channelID, type)

class TextChannel(ServerChannel):
    def __init__(self, channelID: str, server, name: str, **kwargs) -> None:
        self.lastMessageID: str|None = kwargs.get("lastMessageID")
        super().__init__(channelID, ChannelType.TextChannel, server, name, **kwargs)

class VoiceChannel(ServerChannel):
    def __init__(self, channelID: str, server, name: str, **kwargs) -> None:
        super().__init__(channelID, ChannelType.VoiceChannel, server, name, **kwargs)