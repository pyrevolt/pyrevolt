import asyncio
from .session import Session

class Bot:
    async def start(self, *args, **kwargs) -> None:
        self.session: Session = Session()
        await self.session.Start(kwargs["token"])
        while True:
            await self.session.GatewayReceive()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.Close()

    def run(self, *args, **kwargs) -> None:
        async def runner():
            async with self:
                await self.start(*args, **kwargs)
        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            return