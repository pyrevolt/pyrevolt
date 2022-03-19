from typing import List

class Authenticate:
    VALUE = "Authenticate"

class BeginTyping:
    VALUE = "BeginTyping"

class EndTyping:
    VALUE = "EndTyping"

class Ping:
    VALUE = "Ping"

class Event:
    LISTENERS: List[callable] = []

    def __call__(self, *args, **kwargs) -> None:
        self.insertListener(args[0])

    def insertListener(self, callback: callable) -> None:
        self.LISTENERS.append(callback)

    async def dispatch(self, *args, **kwargs) -> None:
        for listener in self.LISTENERS:
            await listener(*args, **kwargs)

class Error(Event):
    VALUE = "Error"
    LISTENERS: List[callable] = []

class Authenticated(Event):
    VALUE = "Authenticated"
    LISTENERS: List[callable] = []

class Pong(Event):
    VALUE = "Pong"
    LISTENERS: List[callable] = []

class Ready(Event):
    VALUE = "Ready"
    LISTENERS: List[callable] = []

class Message(Event):
    VALUE = "Message"
    LISTENERS: List[callable] = []

class MessageUpdate(Event):
    VALUE = "MessageUpdate"
    LISTENERS: List[callable] = []

class MessageDelete(Event):
    VALUE = "MessageDelete"
    LISTENERS: List[callable] = []

class ChannelCreate(Event):
    VALUE = "ChannelCreate"
    LISTENERS: List[callable] = []

class ChannelUpdate(Event):
    VALUE = "ChannelUpdate"
    LISTENERS: List[callable] = []

class ChannelDelete(Event):
    VALUE = "ChannelDelete"
    LISTENERS: List[callable] = []

class ChannelGroupJoin(Event):
    VALUE = "ChannelGroupJoin"
    LISTENERS: List[callable] = []

class ChannelGroupLeave(Event):
    VALUE = "ChannelGroupLeave"
    LISTENERS: List[callable] = []

class ChannelStartTyping(Event):
    VALUE = "ChannelStartTyping"
    LISTENERS: List[callable] = []

class ChannelStopTyping(Event):
    VALUE = "ChannelStopTyping"
    LISTENERS: List[callable] = []

class ChannelAck(Event):
    VALUE = "ChannelAck"
    LISTENERS: List[callable] = []

class ServerUpdate(Event):
    VALUE = "ServerUpdate"
    LISTENERS: List[callable] = []

class ServerDelete(Event):
    VALUE = "ServerDelete"
    LISTENERS: List[callable] = []

class ServerMemberUpdate(Event):
    VALUE = "ServerMemberUpdate"
    LISTENERS: List[callable] = []

class ServerMemberJoin(Event):
    VALUE = "ServerMemberJoin"
    LISTENERS: List[callable] = []

class ServerMemberLeave(Event):
    VALUE = "ServerMemberLeave"
    LISTENERS: List[callable] = []

class ServerRoleUpdate(Event):
    VALUE = "ServerRoleUpdate"
    LISTENERS: List[callable] = []

class ServerRoleDelete(Event):
    VALUE = "ServerRoleDelete"
    LISTENERS: List[callable] = []

class UserUpdate(Event):
    VALUE = "UserUpdate"
    LISTENERS: List[callable] = []

class UserRelationship(Event):
    VALUE = "UserRelationship"
    LISTENERS: List[callable] = []