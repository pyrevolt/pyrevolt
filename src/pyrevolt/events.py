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
    LISTENERS: list[callable] = []

    def __call__(self, *args, **kwargs) -> None:
        self.insertListener(args[0])

    def insertListener(self, callback: callable) -> None:
        self.LISTENERS.append(callback)

    async def dispatch(self, *args, **kwargs) -> None:
        for listener in self.LISTENERS:
            await listener(*args, **kwargs)

class Error(Event):
    VALUE = "Error"
    LISTENERS: list[callable] = []

class Authenticated(Event):
    VALUE = "Authenticated"
    LISTENERS: list[callable] = []

class Pong(Event):
    VALUE = "Pong"
    LISTENERS: list[callable] = []

class Ready(Event):
    VALUE = "Ready"
    LISTENERS: list[callable] = []

class OnMessage(Event):
    VALUE = "Message"
    LISTENERS: list[callable] = []

class MessageUpdate(Event):
    VALUE = "MessageUpdate"
    LISTENERS: list[callable] = []

class MessageDelete(Event):
    VALUE = "MessageDelete"
    LISTENERS: list[callable] = []

class ChannelCreate(Event):
    VALUE = "ChannelCreate"
    LISTENERS: list[callable] = []

class ChannelUpdate(Event):
    VALUE = "ChannelUpdate"
    LISTENERS: list[callable] = []

class ChannelDelete(Event):
    VALUE = "ChannelDelete"
    LISTENERS: list[callable] = []

class ChannelGroupJoin(Event):
    VALUE = "ChannelGroupJoin"
    LISTENERS: list[callable] = []

class ChannelGroupLeave(Event):
    VALUE = "ChannelGroupLeave"
    LISTENERS: list[callable] = []

class ChannelStartTyping(Event):
    VALUE = "ChannelStartTyping"
    LISTENERS: list[callable] = []

class ChannelStopTyping(Event):
    VALUE = "ChannelStopTyping"
    LISTENERS: list[callable] = []

class ChannelAck(Event):
    VALUE = "ChannelAck"
    LISTENERS: list[callable] = []

class ServerUpdate(Event):
    VALUE = "ServerUpdate"
    LISTENERS: list[callable] = []

class ServerDelete(Event):
    VALUE = "ServerDelete"
    LISTENERS: list[callable] = []

class ServerMemberUpdate(Event):
    VALUE = "ServerMemberUpdate"
    LISTENERS: list[callable] = []

class ServerMemberJoin(Event):
    VALUE = "ServerMemberJoin"
    LISTENERS: list[callable] = []

class ServerMemberLeave(Event):
    VALUE = "ServerMemberLeave"
    LISTENERS: list[callable] = []

class ServerRoleUpdate(Event):
    VALUE = "ServerRoleUpdate"
    LISTENERS: list[callable] = []

class ServerRoleDelete(Event):
    VALUE = "ServerRoleDelete"
    LISTENERS: list[callable] = []

class UserUpdate(Event):
    VALUE = "UserUpdate"
    LISTENERS: list[callable] = []

class UserRelationship(Event):
    VALUE = "UserRelationship"
    LISTENERS: list[callable] = []