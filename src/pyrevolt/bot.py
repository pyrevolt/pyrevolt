from __future__ import annotations
import asyncio
import inspect
import json
from typing import Any
from .gateway import GatewayEvent
from .events import OnMessage
from .session import Session
from .structs.channels import Channel, Message

class Bot:
    class Commands:
        def __init__(self, bot: Bot, **kwargs) -> None:
            self.commandListeners: dict[str, dict[callable]] = {}
            self.errorListeners: dict[str, dict[callable]] = {}
            self.bot: Bot = bot
            self.prefix: str = kwargs.get("prefix")

        def Error(self, **kwargs) -> None:
            def decorator(func: callable) -> callable:
                self.errorListeners[kwargs["name"]] = []
                self.errorListeners[kwargs["name"]].append(func)
                return func
            return decorator

        def Command(self, **kwargs) -> None:
            def decorator(func: callable) -> callable:
                func.error = self.Error(**kwargs)
                listeners: dict[callable] = self.commandListeners.get(kwargs["name"], [])
                listeners.append(func)
                self.commandListeners[kwargs["name"]] = listeners
                for alias in kwargs.get("aliases", []):
                    listeners: dict[callable] = self.commandListeners.get(alias, [])
                    listeners.append(func)
                    self.commandListeners[alias] = listeners
                return func
            return decorator

        async def DispatchCommand(self, message: Message) -> None:
            if message.content.startswith(self.prefix):
                arguments: dict[str] = message.content.split(" ")
                command: str = arguments[0][len(self.prefix):]
                if command in self.commandListeners:
                    args: tuple(Any) = tuple(arguments[1:])
                    for func in self.commandListeners[command]:
                        try:
                            await func(message, *args)
                        except Exception as error:
                            if command in self.errorListeners:
                                for func in self.errorListeners[command]:
                                    await func(message, error)

    def __init__(self, **kwargs) -> None:
        self.commands = self.Commands(self, prefix=kwargs.get("prefix"))

    async def Start(self, *args, **kwargs) -> None:
        self.session: Session = Session()
        await self.session.Start(kwargs["token"])
        while True:
            data: dict = await self.session.GatewayReceive()
            if data["type"] == GatewayEvent.OnMessage.value:
                data["type"] = None
                context: Message = await Message.FromJSON(json.dumps(data), self.session)
                await self.commands.DispatchCommand(context)

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