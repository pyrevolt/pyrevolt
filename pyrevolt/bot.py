from __future__ import annotations
import asyncio
import json
from typing import Any
from .structs.invite import Invite
from .structs.member import Member
from .exceptions import InvalidSession
from .gateway import GatewayEvent
from .session import Session
from .structs.channels import Channel, Message
from .structs.user import User
from .structs.server import Server, Role

class Bot:
    class Commands:
        def __init__(self, bot: Bot, **kwargs) -> None:
            self.commandListeners: dict[callable, dict[str, list[str]]] = {}
            self.errorListeners: dict[callable, list[callable]] = {}
            self.bot: Bot = bot
            self.prefix: str = kwargs.get("prefix", "")

        def Command(self, **kwargs) -> callable:
            def decorator(func: callable) -> callable:
                func.Error = self.Error(**kwargs)
                self.commandListeners[func] = {}
                triggers: list[str] = [kwargs["name"]]
                for alias in kwargs.get("aliases", []):
                    triggers.append(alias)
                self.commandListeners[func]["triggers"] = triggers
                return func
            return decorator

        def Error(self, **kwargs) -> callable:
            def decorator(func: callable) -> callable:
                for listener in self.commandListeners:
                    if kwargs["name"] in self.commandListeners[listener]["triggers"]:
                        errors = self.commandListeners[listener].get("errors", [])
                        errors.append(func)
                        self.commandListeners[listener]["errors"] = errors
                return func
            return decorator

        async def dispatchCommand(self, context: Message) -> None:
            if not isinstance(context.content, str):
                return
            if context.content.startswith(self.prefix):
                arguments: list[str] = context.content.split(" ")
                command: str = arguments[0][len(self.prefix):]

                for listener in self.commandListeners:
                    if command in self.commandListeners[listener]["triggers"]:
                        for arg in arguments[1:]:
                            # Attempt to parse argument as channel, user, or role
                            channel: bool|Channel = await Channel.AttemptParse(arg, self.bot.session)
                            if channel is not False:
                                arguments[arguments.index(arg)] = channel
                            user: bool|User = await User.AttemptParse(arg, self.bot.session)
                            if user is not False:
                                arguments[arguments.index(arg)] = user
                        try:
                            await listener(context, *tuple(arguments[1:]))
                        except Exception as error:
                            for errorListener in self.commandListeners[listener].get("errors", []):
                                await errorListener(context, error)
                        break

    def __init__(self, **kwargs) -> None:
        self.commands = self.Commands(self, prefix=kwargs.get("prefix"))

    async def Start(self, **kwargs) -> None:
        self.session: Session = Session()
        if kwargs.get("token") is None:
            raise InvalidSession("No token provided")
        await self.session.Start(kwargs["token"])
        while True:
            data: dict = await self.session.GatewayReceive()
            if data["type"] == GatewayEvent.OnMessage.value:
                data["type"] = None
                context: Message = await Message.FromJSON(json.dumps(data), self.session)
                await self.commands.dispatchCommand(context)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.Close()

    def Run(self, **kwargs) -> None:
        async def runner():
            async with self:
                await self.Start(**kwargs)
        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            return

    def on(self, event: GatewayEvent) -> callable:
        def decorator(func: callable):
            event.value.insertListener(func)
            return func
        return decorator

    async def GetUser(self, userID: str) -> User:
        return await self.session.GetUser(userID)

    async def GetChannel(self, channelID: str) -> Channel:
        return await self.session.GetChannel(channelID)

    async def GetMessage(self, channelID: str, messageID: str) -> Message:
        return await self.session.GetMessage(channelID, messageID)
    
    async def GetServer(self, serverID: str) -> Server:
        return await self.session.GetServer(serverID)

    async def GetMember(self, memberID: str) -> Member:
        ids: str = memberID.split(".")
        return await self.session.GetMember(ids[0], ids[1])

    async def GetMemberFromServer(self, serverID: str, userID: str) -> Member|None:
        return await self.session.GetMember(serverID, userID)

    async def GetRole(self, serverID: str, roleID: str) -> Role:
        return await self.session.GetRole(serverID, roleID)

    async def GetInvite(self, inviteID: str) -> Invite:
        return await self.session.GetInvite(inviteID)