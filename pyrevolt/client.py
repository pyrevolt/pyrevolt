from enum import Enum
from aiohttp import ClientSession
from .exceptions import ClosedSocketException

class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE  = "DELETE"
    PATCH = "PATCH"

class Request:
    API_BASE_URL = "https://api.revolt.chat"
    
    def __init__(self, method: Method, url: str, *args, **kwargs) -> None:
        self.method = method
        self.url = f"{self.API_BASE_URL}{url}"
        self.data = kwargs.get("data", dict())
        self.headers = kwargs.get("headers", dict())
        self.params = kwargs.get("params", dict())
        if kwargs.get("auth") is not None:
            self.AddAuthentication(kwargs.get("auth"))

    def AddAuthentication(self, token: str, bot: bool = True) -> None:
        if bot:
            self.headers["x-bot-token"] = token
        else:
            self.headers["x-session-token"] = token

class HTTPClient:
    def __init__(self) -> None:
        self.client = ClientSession()

    async def close(self) -> None:
        await self.client.close()

    async def request(self, request: Request) -> dict:
        if not self.client.closed:
            async with self.client.request(
            method = request.method.value,
            url = request.url,
            data = request.data,
            headers = request.headers,
            params = request.params) as result:
                # TODO: Add status code check
                return await result.json()
        else:
            raise ClosedSocketException()
