from enum import Enum
import json
from typing import Any
from aiohttp import ClientSession
from .exceptions import ClosedSocketException

class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE  = "DELETE"
    PATCH = "PATCH"

class Request:
    API_BASE_URL: str = "https://api.revolt.chat"
    
    def __init__(self, method: Method, url: str, **kwargs) -> None:
        self.method: Method = method
        self.url: str = f"{self.API_BASE_URL}{url}"
        self.data: dict[str, Any] = kwargs.get("data", dict())
        self.headers: dict[str, str] = kwargs.get("headers", dict())
        self.params: dict[str, Any] = kwargs.get("params", dict())
        if kwargs.get("auth") is not None:
            self.AddAuthentication(kwargs.get("auth"))

    def AddAuthentication(self, token: str, bot: bool = True) -> None:
        if bot:
            self.headers["x-bot-token"] = token
        else:
            self.headers["x-session-token"] = token

class HTTPClient:
    def __init__(self) -> None:
        self.client: ClientSession = ClientSession()

    async def Close(self) -> None:
        await self.client.close()

    async def Request(self, request: Request) -> dict:
        if not self.client.closed:
            async with self.client.request(
                method = request.method.value,
                url = request.url,
                data = json.dumps(request.data),
                headers = request.headers,
                params = request.params
            ) as result:
                # TODO: Add status code check
                return await result.json()
        else:
            raise ClosedSocketException()
