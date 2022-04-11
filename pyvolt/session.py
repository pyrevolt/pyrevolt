import json
from .client import HTTPClient
from .gateway import Gateway, GatewayEvent
from .structs.channels import Channel
from .structs.user import User

class Session:
    def __init__(self) -> None:
        self.gateway: Gateway = Gateway()
        self.client: HTTPClient = HTTPClient()
        self.token: str|None = None
        self.users: dict[str, User] = {}
        self.channels: dict[str, Channel] = {}

    async def Connect(self) -> None:
        await self.gateway.Connect()

    async def Start(self, token: str) -> None:
        await self.Connect()
        await self.gateway.Authenticate(token)
        self.token = token

    async def Close(self) -> None:
        await self.gateway.Close()
        await self.client.Close()
    
    async def GatewayReceive(self) -> dict:
        data: dict = await self.gateway.Receive()
        for event in GatewayEvent:
            if data["type"] == event.value.VALUE:
                data["type"] = event.value
                break
        match data["type"]:
            case GatewayEvent.Ready.value:
                for index, user in enumerate(data["users"]):
                    user: User = await User.FromJSON(json.dumps(user))
                    data["users"][index] = user
                    self.users[user.userID] = user
                for index, channel in enumerate(data["channels"]):
                    channel: Channel = await Channel.FromJSON(json.dumps(channel), self)
                    data["channels"][index] = channel
                    self.channels[channel.channelID] = channel
            case GatewayEvent.UserUpdate.value:
                user: User | None = self.users.get(data["id"])
                if user is not None:
                    await user.Update(data["data"])
                    
        await data["type"].dispatch()
        return data