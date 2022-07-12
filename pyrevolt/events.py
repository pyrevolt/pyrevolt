class Authenticate:
    VALUE = "Authenticate"

class BeginTyping:
    VALUE = "BeginTyping"

class EndTyping:
    VALUE = "EndTyping"

class Ping:
    VALUE = "Ping"

class Bulk:
    VALUE = "Bulk"

class Event:
    def __init__(self) -> None:
        self.listeners: list[callable] = []

    def __call__(self, *args, **kwargs) -> None:
        self.insertListener(args[0])

    def insertListener(self, callback: callable) -> None:
        self.listeners.append(callback)

    async def dispatch(self, *args, **kwargs) -> None:
        for listener in self.listeners:
            await listener(*args, **kwargs)

class Error(Event):
    VALUE = "Error"

class Authenticated(Event):
    VALUE = "Authenticated"

class Pong(Event):
    VALUE = "Pong"

class Ready(Event):
    VALUE = "Ready"

class ReadySimplified(Event):
    VALUE = "ReadySimplified"

class OnMessage(Event):
    VALUE = "Message"

class MessageUpdate(Event):
    VALUE = "MessageUpdate"

class MessageDelete(Event):
    VALUE = "MessageDelete"

class ChannelCreate(Event):
    VALUE = "ChannelCreate"

class ChannelUpdate(Event):
    VALUE = "ChannelUpdate"

class ChannelDelete(Event):
    VALUE = "ChannelDelete"

class ChannelGroupJoin(Event):
    VALUE = "ChannelGroupJoin"

class ChannelGroupLeave(Event):
    VALUE = "ChannelGroupLeave"

class ChannelStartTyping(Event):
    VALUE = "ChannelStartTyping"

class ChannelStopTyping(Event):
    VALUE = "ChannelStopTyping"

class ChannelAck(Event):
    VALUE = "ChannelAck"

class ServerCreate(Event):
    VALUE = "ServerCreate"

class ServerUpdate(Event):
    VALUE = "ServerUpdate"

class ServerDelete(Event):
    VALUE = "ServerDelete"

class ServerMemberUpdate(Event):
    VALUE = "ServerMemberUpdate"

class ServerMemberJoin(Event):
    VALUE = "ServerMemberJoin"

class ServerMemberLeave(Event):
    VALUE = "ServerMemberLeave"

class ServerRoleUpdate(Event):
    VALUE = "ServerRoleUpdate"

class ServerRoleDelete(Event):
    VALUE = "ServerRoleDelete"

class UserUpdate(Event):
    VALUE = "UserUpdate"

class UserRelationship(Event):
    VALUE = "UserRelationship"