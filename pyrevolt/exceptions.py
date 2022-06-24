class WebsocketError(Exception):
    pass

class InternalWebsocketError(WebsocketError):
    pass

class InvalidSession(WebsocketError):
    pass

class OnboardingNotFinished(WebsocketError):
    pass

class AlreadyAuthenticated(WebsocketError):
    pass

class ClosedSocketException(WebsocketError):
    pass

class InvalidMessageException(Exception):
    pass


class RequestError(Exception):
    pass

class InternalServerError(RequestError):
    pass

class InvalidRequest(RequestError):
    pass

class AlreadyOnboarded(RequestError):
    pass

class UsernameTaken(RequestError):
    pass

class InvalidUsername(RequestError):
    pass

class UnknownUser(RequestError):
    pass

class AlreadyFriends(RequestError):
    pass

class AlreadySentRequest(RequestError):
    pass

class Blocked(RequestError):
    pass

class BlockedByOther(RequestError):
    pass

class NotFriends(RequestError):
    pass

class UnknownChannel(RequestError):
    pass

class UnknownAttachment(RequestError):
    pass

class UnknownMessage(RequestError):
    pass

class CannotEditMessage(RequestError):
    pass

class CannotJoinCall(RequestError):
    pass

class TooManyAttachments(RequestError):
    pass

class TooManyReplies(RequestError):
    pass

class EmptyMessage(RequestError):
    pass

class PayloadTooLarge(RequestError):
    pass

class CannotRemoveYourself(RequestError):
    pass

class GroupTooLarge(RequestError):
    pass

class AlreadyInGroup(RequestError):
    pass

class NotInGroup(RequestError):
    pass

class UnknownServer(RequestError):
    pass

class InvalidRole(RequestError):
    pass

class Banned(RequestError):
    pass

class TooManyServers(RequestError):
    pass

class ReachedMaximumBots(RequestError):
    pass

class IsBot(RequestError):
    pass

class BotIsPrivate(RequestError):
    pass

class MissingPermission(RequestError):
    pass

class MissingUserPermission(MissingPermission):
    pass

class NotElevated(RequestError):
    pass

class CannotGiveMissingPermissions(RequestError):
    pass

class DatabaseError(InternalServerError):
    pass

class InvalidOperation(RequestError):
    pass

class InvalidCredentials(RequestError):
    pass

class InvalidSession(RequestError):
    pass

class DuplicateNonce(RequestError):
    pass

class VosoUnavailable(RequestError):
    pass

class NotFound(RequestError):
    pass

class NoEffect(RequestError):
    pass

class FailedValidation(RequestError):
    pass