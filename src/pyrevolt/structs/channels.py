from __future__ import annotations
from enum import Enum
import json
from ..client import Method
from .user import User
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .messaging import Embed, Masquerade
    from ..session import Session

class ChannelType(Enum):
    SavedMessages = "SavedMessages"
    DirectMessage = "DirectMessage"
    Group = "Group"
    TextChannel = "TextChannel"
    VoiceChannel = "VoiceChannel"

class Channel:
    def __init__(self, channelID: str, type: ChannelType, **kwargs) -> None:
        self.channelID: str = channelID
        self.type: ChannelType = type
        self.session = kwargs.get("session")

    @staticmethod
    async def FromJSON(jsonData: str|bytes, session: Session) -> Channel:
        data: dict = json.loads(jsonData)
        kwargs: dict = {}
        kwargs["session"] = session
        channel: Channel = None
        match data["channel_type"]:
            case ChannelType.SavedMessages.value:
                user: User|None = session.users.get(data["user"])
                if user is None:
                    user = await User.FromID(data["user"], session.token)
                channel = SavedMessages(data["_id"], user)
            case ChannelType.DirectMessage.value:
                if data.get("last_message_id") is not None:
                    kwargs["lastMessageID"] = data["last_message_id"]
                recipients: dict[User] = []
                for userID in data["recipients"]:
                    user: User|None = session.users.get(userID)
                    if user is None:
                        user = await User.FromID(userID, session.token)
                    recipients.append(user)
                channel = DirectMessage(data["_id"], data["active"], recipients, **kwargs)
            case ChannelType.Group.value:
                if data.get("description") is not None:
                    kwargs["description"] = data["description"]
                if data.get("last_message_id") is not None:
                    kwargs["lastMessageID"] = data["last_message_id"]
                if data.get("permissions") is not None:
                    kwargs["permissions"] = data["permissions"]
                if data.get("nsfw") is not None:
                    kwargs["nsfw"] = data["nsfw"]
                recipients: dict[User] = []
                owner: User = None
                for userID in data["recipients"]:
                    user: User|None = session.users.get(userID)
                    if user is None:
                        user = await User.FromID(userID, session.token)
                    if user.userID == data["owner"]:
                        owner = user
                    recipients.append(user)
                channel = Group(data["_id"], data["name"], recipients, owner, **kwargs)
            case ChannelType.TextChannel.value:
                if data.get("description") is not None:
                    kwargs["description"] = data["description"]
                if data.get("default_permissions") is not None:
                    kwargs["defaultPermissions"] = data["defaultPermissions"]
                if data.get("nsfw") is not None:
                    kwargs["nsfw"] = data["nsfw"]
                if data.get("last_message_id") is not None:
                    kwargs["lastMessageID"] = data["last_message_id"]
                channel = TextChannel(data["_id"], data["server"], data["name"], **kwargs)
            case ChannelType.VoiceChannel.value:
                if data.get("description") is not None:
                    kwargs["description"] = data["description"]
                if data.get("default_permissions") is not None:
                    kwargs["defaultPermissions"] = data["defaultPermissions"]
                if data.get("nsfw") is not None:
                    kwargs["nsfw"] = data["nsfw"]
                channel = VoiceChannel(data["_id"], data["server"], data["name"], **kwargs)
        session.channels[channel.channelID] = channel
        return channel

    @staticmethod
    async def FromID(channelID: str, session: Session) -> Channel:
        if session.channels.get(channelID) is not None:
            return session.channels[channelID]
        result: dict = await session.Request(Method.GET, f"/channels/{channelID}")
        if result.get("type") is not None:
            return
        return await Channel.FromJSON(json.dumps(result), session)

    async def Send(self, message: str) -> None:
        await Message.Send(self, self.session, content=message)

class SavedMessages(Channel):
    def __init__(self, channelID: str, user: User, **kwargs) -> None:
        self.user: User = user
        super().__init__(channelID, ChannelType.SavedMessages, **kwargs)

    def __repr__(self) -> str:
        return f"<pyrevolt.SavedMessage id={self.channelID} user={self.user}>"

class DirectMessage(Channel):
    def __init__(self, channelID: str, active: bool, recipients: dict[User], **kwargs) -> None:
        self.active: bool = active
        self.recipients: dict[User] = recipients
        self.lastMessageID: str|None = kwargs.get("lastMessageID")
        super().__init__(channelID, ChannelType.DirectMessage, **kwargs)

    def __repr__(self) -> str:
        return f"<pyrevolt.DirectMessage id={self.channelID} active={self.active} recipients=[{self.recipients}]>"

class Group(Channel):
    def __init__(self, channelID: str, name: str, recipients: dict[User], owner: User, **kwargs) -> None:
        self.name: str = name
        self.recipients: dict[User] = recipients
        self.owner: User = owner
        self.description: str|None = kwargs.get("description")
        self.lastMessageID: str|None = kwargs.get("lastMessageID")
        # TODO: Icon
        self.permissions: int|None = kwargs.get("permissions")
        self.nsfw: bool|None = kwargs.get("nsfw")
        super().__init__(channelID, ChannelType.Group, **kwargs)

    def __repr__(self) -> str:
        return f"<pyrevolt.Group id={self.channelID} name={self.name} recipients=[{self.recipients}] owner={self.owner}>"

class ServerChannel(Channel):
    def __init__(self, channelID: str, type: ChannelType, server, name: str, **kwargs) -> None:
        self.server = server
        self.name: str = name
        self.description: str | None = kwargs.get("description")
        # TODO: Icon
        self.defaultPermissions: int | None = kwargs.get("defaultPermissions")
        # TODO: Role permissions
        self.nsfw: bool | None = kwargs.get("nsfw")
        super().__init__(channelID, type, **kwargs)

class TextChannel(ServerChannel):
    def __init__(self, channelID: str, server, name: str, **kwargs) -> None:
        self.lastMessageID: str|None = kwargs.get("lastMessageID")
        super().__init__(channelID, ChannelType.TextChannel, server, name, **kwargs)

    def __repr__(self) -> str:
        return f"<pyrevolt.TextChannel id={self.channelID} server={self.server} name={self.name}>"

class VoiceChannel(ServerChannel):
    def __init__(self, channelID: str, server, name: str, **kwargs) -> None:
        super().__init__(channelID, ChannelType.VoiceChannel, server, name, **kwargs)

    def __repr__(self) -> str:
        return f"<pyrevolt.VoiceChannel id={self.channelID} server={self.server} name={self.name}>"


class Message:
    def __init__(self, messageID: str, channel: Channel, author: User, content, **kwargs):
        self.messageID: int = messageID
        self.channel: Channel = channel
        self.author: User = author
        self.content = content
        self.nonce: str | None = kwargs.get("nonce")
        self.edited: str | None = kwargs.get("edited")
        self.embeds: dict[Embed] | None = kwargs.get("embeds")
        self.mentions: dict[User] | None = kwargs.get("mentions")
        self.replies: dict[Message] | None = kwargs.get("replies")
        self.masquerade: Masquerade | None = kwargs.get("masquerade")

    def __repr__(self) -> str:
        return f"<pyrevolt.Message id={self.messageID} channel={self.channel} author={self.author}>"

    @staticmethod
    async def FromJSON(jsonData: str | bytes, session: Session) -> Message:
        data: dict = jsonData
        kwargs: dict = {}
        return Message(data["_id"], await Channel.FromID(data["channel"], session), await User.FromID(data["author"], session), data["content"], **kwargs)

    @staticmethod
    async def Send(channel: Channel, session: Session, **kwargs) -> Message:
        data: dict = {}
        data["content"] = kwargs.get("content", "")
        if kwargs.get("replies") is not None:
            for reply in kwargs["replies"]:
                data["replies"].append(
                    {"id": reply.message.messageID, "mention": reply.mention})
        await Message.FromJSON(await session.Request(Method.POST, f"/channels/{channel.channelID}/messages", data=data), session)
