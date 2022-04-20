import asyncio
from .gateway import GatewayEvent
from .session import Session
from .client import Method
from .structs.channels import Channel

class Bot:
    async def Start(self, *args, **kwargs) -> None:
        self.session: Session = Session()
        await self.session.Start(kwargs["token"])
        while True:
            await self.session.GatewayReceive()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.Close()

    def Run(self, *args, **kwargs) -> None:
        async def runner():
            async with self:
                await self.Start(*args, **kwargs)
        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            return

    def on(self, event: GatewayEvent) -> None:
        def decorator(func: callable):
            event.value.insertListener(func)
            return func
        return decorator

    async def GetChannel(self, channelID: str) -> Channel:
        return await self.session.GetChannel(channelID)