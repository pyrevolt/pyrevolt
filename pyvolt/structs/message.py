from __future__ import annotations
from enum import Enum
import json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pyvolt.structs.channels import Channel
    from pyvolt.structs.user import User

class EmbedType(Enum):
    Website = "Website"
    Image = "Image"
    Text = "Text"

class EmbedImageSize(Enum):
    Large = "Large"
    Preview = "Preview"

class Embed:
    def __init__(self, type: EmbedType | None, **kwargs):
        self.type: EmbedType = type
        match self.type:
            case EmbedType.Website:
                self.url: str|None = kwargs.get("url")
                self.specials: dict|None = kwargs.get("specials")
                self.title: str|None = kwargs.get("title")
                self.description: str|None = kwargs.get("description")
                self.siteName: str|None = kwargs.get("site_name")
                self.icon_url: str|None = kwargs.get("icon_url")
                self.colour: str|None = kwargs.get("colour")
            case EmbedType.Image:
                self.url: str = kwargs["url"]
                self.width: int = kwargs["width"]
                self.height: int = kwargs["height"]
                self.size: EmbedImageSize = kwargs["size"]
            case EmbedType.Text:
                self.iconURL: str|None = kwargs.get("icon_url")
                self.url: str|None = kwargs.get("url")
                self.title: str|None = kwargs.get("title")
                self.description: str|None = kwargs.get("description")
                self.colour: str|None = kwargs.get("colour")
            case None:
                return

class Masquerade:
    def __init__(self, **kwargs):
        self.name: str|None = kwargs.get("name")
        self.avatar: str|None = kwargs.get("avatar")

class Message:
    def __init__(self, messageID: int, channel: Channel, author: User, content, **kwargs):
        self.messageID: int = messageID
        self.channel: Channel = channel
        self.author: User = author
        self.content = content
        self.nonce: str|None = kwargs.get("nonce")
        self.edited: str|None = kwargs.get("edited")
        self.embeds: dict[Embed]|None = kwargs.get("embeds")
        self.mentions: dict[User]|None = kwargs.get("mentions")
        self.replies: dict[Message]|None = kwargs.get("replies")
        self.masquerade: Masquerade|None = kwargs.get("masquerade")
    
    def __repr__(self) -> str:
        return f"<pyvolt.Message id={self.messageID} channel={self.channel} author={self.author}>"
    
    # @staticmethod
    # def Create()