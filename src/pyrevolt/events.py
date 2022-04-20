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
    LISTENERS: dict[callable] = []

    def __call__(self, *args, **kwargs) -> None:
        self.insertListener(args[0])

    def insertListener(self, callback: callable) -> None:
        self.LISTENERS.append(callback)

    async def dispatch(self, *args, **kwargs) -> None:
        for listener in self.LISTENERS:
            await listener(*args, **kwargs)

class Error(Event):
    VALUE = "Error"
    LISTENERS: dict[callable] = []

class Authenticated(Event):
    VALUE = "Authenticated"
    LISTENERS: dict[callable] = []

class Pong(Event):
    VALUE = "Pong"
    LISTENERS: dict[callable] = []

class Ready(Event):
    VALUE = "Ready"
    LISTENERS: dict[callable] = []

class OnMessage(Event):
    VALUE = "Message"
    LISTENERS: dict[callable] = []

class MessageUpdate(Event):
    VALUE = "MessageUpdate"
    LISTENERS: dict[callable] = []

class MessageDelete(Event):
    VALUE = "MessageDelete"
    LISTENERS: dict[callable] = []

class ChannelCreate(Event):
    VALUE = "ChannelCreate"
    LISTENERS: dict[callable] = []

class ChannelUpdate(Event):
    VALUE = "ChannelUpdate"
    LISTENERS: dict[callable] = []

class ChannelDelete(Event):
    VALUE = "ChannelDelete"
    LISTENERS: dict[callable] = []

class ChannelGroupJoin(Event):
    VALUE = "ChannelGroupJoin"
    LISTENERS: dict[callable] = []

class ChannelGroupLeave(Event):
    VALUE = "ChannelGroupLeave"
    LISTENERS: dict[callable] = []

class ChannelStartTyping(Event):
    VALUE = "ChannelStartTyping"
    LISTENERS: dict[callable] = []

class ChannelStopTyping(Event):
    VALUE = "ChannelStopTyping"
    LISTENERS: dict[callable] = []

class ChannelAck(Event):
    VALUE = "ChannelAck"
    LISTENERS: dict[callable] = []

class ServerUpdate(Event):
    VALUE = "ServerUpdate"
    LISTENERS: dict[callable] = []

class ServerDelete(Event):
    VALUE = "ServerDelete"
    LISTENERS: dict[callable] = []

class ServerMemberUpdate(Event):
    VALUE = "ServerMemberUpdate"
    LISTENERS: dict[callable] = []

class ServerMemberJoin(Event):
    VALUE = "ServerMemberJoin"
    LISTENERS: dict[callable] = []

class ServerMemberLeave(Event):
    VALUE = "ServerMemberLeave"
    LISTENERS: dict[callable] = []

class ServerRoleUpdate(Event):
    VALUE = "ServerRoleUpdate"
    LISTENERS: dict[callable] = []

class ServerRoleDelete(Event):
    VALUE = "ServerRoleDelete"
    LISTENERS: dict[callable] = []

class UserUpdate(Event):
    VALUE = "UserUpdate"
    LISTENERS: dict[callable] = []

class UserRelationship(Event):
    VALUE = "UserRelationship"
    LISTENERS: dict[callable] = []