import json
from typing import List
from .client import HTTPClient
from .gateway import Gateway, GatewayEvent
from .structs.user import User

class Session:
    def __init__(self) -> None:
        self.gateway: Gateway = Gateway()
        self.client: HTTPClient = HTTPClient()
        self.token: str|None = None
        self.members: List[User] = []

    async def Connect(self) -> None:
        await self.gateway.Connect()

    async def Start(self, token: str) -> None:
        await self.Connect()
        await self.gateway.Authenticate(token)
        self.token = token#

    async def Close(self) -> None:
        await self.gateway.Close()
        await self.client.Close()
    
    async def GatewayReceive(self) -> dict:
        data = await self.gateway.Receive()
        for event in GatewayEvent:
            if data["type"] == event.value.VALUE:
                data["type"] = event.value
                break
        match data["type"]:
            case GatewayEvent.Ready.value:
                for index, user in enumerate(data["users"]):
                    data["users"][index] = await User.FromJSON(json.dumps(user))
                    self.members.append(data["users"][index])
        await data["type"].dispatch()
        return data