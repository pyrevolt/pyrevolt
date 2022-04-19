from __future__ import annotations
from enum import Enum
import json
from typing import TYPE_CHECKING
from src.pyrevolt.client import Method
if TYPE_CHECKING:
    from .channels import Message
    from .user import User
    from ..session import Session

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

class Reply:
    def __init__(self, message: Message, mention: bool):
        self.message: Message = message
        self.mention: bool = mention