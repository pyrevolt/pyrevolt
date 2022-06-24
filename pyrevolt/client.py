from enum import Enum
import json
from typing import Any
from aiohttp import ClientSession
from .exceptions import *

class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

class Request:
    API_BASE_URL: str = "https://api.revolt.chat"
    
    def __init__(self, method: Method, url: str, **kwargs) -> None:
        self.method: Method = method
        self.url: str = f"{self.API_BASE_URL}{url}"
        self.data: dict[str, Any] = kwargs.get("data", dict())
        self.headers: dict[str, str] = kwargs.get("headers", dict())
        self.params: dict[str, Any] = kwargs.get("params", dict())
        if kwargs.get("auth") is not None:
            self.AddAuthentication(kwargs.get("auth"))

    def AddAuthentication(self, token: str, bot: bool = True) -> None:
        if bot:
            self.headers["x-bot-token"] = token
        else:
            self.headers["x-session-token"] = token

class HTTPClient:
    def __init__(self) -> None:
        self.client: ClientSession = ClientSession()

    async def Close(self) -> None:
        await self.client.close()

    async def Request(self, request: Request) -> dict:
        if not self.client.closed:
            async with self.client.request(
                method = request.method.value,
                url = request.url,
                data = json.dumps(request.data),
                headers = request.headers,
                params = request.params
            ) as result:
                if result.status == 204:
                    return
                results: dict = await result.json()
                if results.get("type") is not None:
                    match results["type"]:
                        case "LabelMe":
                            raise InternalServerError("A unlabeled server error occured")
                        case "AlreadyOnboarded":
                            raise AlreadyOnboarded()
                        case "UsernameTaken":
                            raise UsernameTaken("Username is already taken")
                        case "InvalidUsername":
                            raise InvalidUsername("Username is invalid")
                        case "UnknownUser":
                            raise UnknownUser("User does not exist")
                        case "AlreadyFriends":
                            raise AlreadyFriends("User is already your friend")
                        case "AlreadySentRequest":
                            raise AlreadySentRequest("You have already sent a friend request to this user")
                        case "Blocked":
                            raise Blocked("User is blocked")
                        case "BlockedByOther":
                            raise BlockedByOther("You have been blocked by this user")
                        case "NotFriends":
                            raise NotFriends("You are not friends with this user")
                        case "UnknownChannel":
                            raise UnknownChannel("Channel does not exist")
                        case "UnknownAttachment":
                            raise UnknownAttachment("Attachment does not exist")
                        case "UnknownMessage":
                            raise UnknownMessage("Message does not exist")
                        case "CannotEditMessage":
                            raise CannotEditMessage("You cannot edit this message")
                        case "CannotJoinCall":
                            raise CannotJoinCall("You cannot join this call")
                        case "TooManyAttachments":
                            raise TooManyAttachments("Too many attachments were sent")
                        case "TooManyReplies":
                            raise TooManyReplies("Too many replies were sent")
                        case "EmptyMessage":
                            raise EmptyMessage("Message is empty")
                        case "PayloadTooLarge":
                            raise PayloadTooLarge("Payload is too large")
                        case "CannotRemoveYourself":
                            raise CannotRemoveYourself("You cannot remove yourself")
                        case "GroupTooLarge":
                            raise GroupTooLarge(f"The group is too large, only a maximum of {results['max']} are allowed")
                        case "AlreadyInGroup":
                            raise AlreadyInGroup("You are already in this group")
                        case "NotInGroup":
                            raise NotInGroup("You are not in this group")
                        case "UnknownServer":
                            raise UnknownServer("Server does not exist")
                        case "InvalidRole":
                            raise InvalidRole("Role is invalid")
                        case "Banned":
                            raise Banned("You have been banned from this server")
                        case "TooManyServers":
                            raise TooManyServers(f"You have too many servers, only a maximum of {results['max']} are allowed")
                        case "ReachedMaximumBots":
                            raise ReachedMaximumBots("You have reached the maximum number of bots")
                        case "IsBot":
                            raise IsBot("This user is a bot")
                        case "BotIsPrivate":
                            raise BotIsPrivate("This bot is private, and cannot be invited")
                        case "MissingPermission":
                            raise MissingPermission(f"You are missing the {results['permission']} permission to perform this action")
                        case "MissingUserPermission":
                            raise MissingUserPermission(f"You are missing the {results['permission']} permission to perform this action")
                        case "NotElevated":
                            raise NotElevated("You are not elevated")
                        case "CannotGiveMissingPermissions":
                            raise CannotGiveMissingPermissions("You cannot give missing permissions")
                        case "DatabaseError":
                            raise DatabaseError(f"A database error occured while attempting the operation {results['operation']} with {results['with']}")
                        case "InvalidOperation":
                            raise InvalidOperation()
                        case "InvalidCredentials":
                            raise InvalidCredentials()
                        case "InvalidSession":
                            raise InvalidSession()
                        case "DuplicateNonce":
                            raise DuplicateNonce()
                        case "VosoUnavailable":
                            raise VosoUnavailable()
                        case "NotFound":
                            raise NotFound()
                        case "NoEffect":
                            raise NoEffect()
                        case "FailedValidation":
                            raise FailedValidation()                            
                return results
        else:
            raise ClosedSocketException()
