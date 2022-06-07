.. currentmodule:: pyrevolt

API
===

Client
~~~~~~

Method
------
.. class:: Method
    
    Bases: :class:`enum.Enum`

    Values:
        - GET
        - POST
        - PUT
        - DELETE
        - PATCH

Request
-------
.. class:: Request(method, url, **kwargs)
    
    A request to be sent to the server. The URL should include the leading slash.

    :param method:
    :type method: :class:`Method`
        The HTTP method to use when sending the request
    :param url:
    :type url: :class:`str`
        The URL to send the request to.
    :param kwargs:
        - ``data``: *Optional* - POST data to be sent.
        - ``headers``: *Optional* - HTTP headers to be sent.
        - ``params``: *Optional* - GET parameters to be sent.
    :returns: :class:`Request`
        The request object.

    .. method:: AddAuthentication(token, bot)
        
            Adds authentication to the request.
    
            :param token:
            :type token: :class:`str`
                The bot token.
            :param bot:
            :type bot: :class:`bool`
                Whether the request is made to be executed by a bot.
            :returns None:
                None

HTTPClient
----------
.. class:: HTTPClient()

    A client for sending requests to the server.

    :returns: :class:`HTTPClient`
        The client object.

    .. method:: Request(request)
        
            *This method is a coroutine.*

            Sends a request to the given request URL.

            :param request:
            :type request: :class:`Request`
                The request to send.
            :returns: :class:`dict`
                The JSON response from the server.

    .. method:: Close()

            *This method is a coroutine.*

            Closes the client.

            :returns None:
                None

Gateway
~~~~~~~

GatewayEvent
------------
.. class:: GatewayEvent
    
    Bases: :class:`enum.Enum`

    Values:
        - Authenticate
        - BeginTyping
        - EndTyping
        - Ping
        - Error
        - Authenticated
        - Bulk
        - Pong
        - Ready
        - ReadySimplified
        - OnMessage
        - MessageUpdate
        - MessageDelete
        - ChannelCreate
        - ChannelUpdate
        - ChannelDelete
        - ChannelGroupJoin
        - ChannelGroupLeave
        - ChannelStartTyping
        - ChannelStopTyping
        - ChannelAck
        - ServerCreate
        - ServerUpdate
        - ServerDelete
        - ServerMemberJoin
        - ServerMemberLeave
        - ServerMemberUpdate
        - ServerRoleUpdate
        - ServerRoleDelete
        - UserUpdate
        - UserRelationship

GatewayKeepAlive
----------------
.. class:: GatewayKeepAlive(*args, gateway, interval, **kwargs)

    Bases: :class:`threading.Thread`

    A thread that keeps the gateway alive by sending a ping for every defined interval.

    :param args:
    :type args: :class:`tuple`
        The arguments to pass to the thread.
    :param gateway:
    :type gateway: :class:`Gateway`
        The gateway to keep alive.
    :param interval:
    :type interval: :class:`float`
        The interval in seconds to send a ping.
    :param kwargs:
        The keyword arguments to pass to the thread.
    :return GatewayKeepAlive:
        The gateway keep alive thread.

    .. method:: run()

        The thread's main run loop. This method executes a ping every ``interval`` seconds.

        :returns None:
            None

    .. method:: GetPayload()

        Gets the payload to send to the gateway.

        :returns: :class:`dict`
            The payload to send to the gateway.

Gateway
-------
.. class:: Gateway()

    A gateway to connect to the Revolt API.

    :returns: :class:`Gateway`
        The gateway object.

    .. method:: GetWebsocketURL()

        *This method is a coroutine.*

        Gets the websocket URL to connect to from the Revolt API. This method is automatically called
        before connecting.

        :returns: :class:`str`
            The websocket URL to connect to.

    .. method:: Connect()

        *This method is a coroutine.*

        Connects to the websocket and starts the `GatewayKeepAlive` thread.

        :returns None:
            None

    .. method:: Close()

        *This method is a coroutine.*

        Closes the websocket and stops the `GatewayKeepAlive` thread.

        :returns None:
            None

    .. method:: Send(payload)

        *This method is a coroutine.*

        Sends a payload to the websocket.

        :param payload:
        :type payload: :class:`dict`
            The payload to send.
        :returns None:
            None

    .. method:: Receive()

        *This method is a coroutine.*

        Receives a payload from the websocket.

        :returns: :class:`dict`
            The payload received from the websocket.

    .. method:: Authenticate(token)

        *This method is a coroutine.*

        Authenticates the gateway with an existing token.

        :param token:
        :type token: :class:`str`
            The bot token.
        :returns None:
            None

Structures
~~~~~~~~~~

User
----

Relationship
^^^^^^^^^^^^
.. class:: Relationship
    
    Bases: :class:`enum.Enum`

    Values:
        - Blocked
        - BlockedOther
        - Friend
        - Incoming
        - Outgoing
        - NoRelationship
        - User

Presence
^^^^^^^^
.. class:: Presence
    
    Bases: :class:`enum.Enum`

    Values:
        - Busy
        - Idle
        - Invisible
        - Online

Status
^^^^^^
.. class:: Status(presence, **kwargs)

    The status a user can have. This includes their presence and any custom text.

    :param presence:
    :type presence: :class:`Presence`
        The presence of the user.
    :param kwargs:
        - ``text``: *Optional* - The custom text of the status.
    
    .. method:: __repr__()

        Gets the string representation of the status.

        :returns: :class:`str`
            The string representation of the status.
            
            ``<pyrevolt.Status presence={self.presence.value} text={self.text}>``

    .. staticmethod:: FromJSON(data)
            
        *This method is a coroutine.*

        Creates a status from a JSON object.

        :param data:
        :type data: :class:`dict`
            The JSON object.
        :returns: :class:`Status`
            The status.

BotUser
^^^^^^^
.. class:: BotUser(ownerID)

    A bot user.

    :param ownerID:
    :type ownerID: :class:`str`
        The ID of the bot owner.
    :returns: :class:`BotUser`
        The bot user.

    .. method:: __repr__()

        Gets the string representation of the bot user.

        :returns: :class:`str`
            The string representation of the bot user.
            
            ``<pyrevolt.Bot owner={self.ownerID}>``

User
^^^^
.. class:: User(userID, username, **kwargs)

    A user.

    :param userID:
    :type userID: :class:`str`
        The ID of the user.
    :param username:
    :type username: :class:`str`
        The username of the user.
    :param kwargs:
        - ``badges``: *Optional* - The badges of the user in `int` form.
        - ``online``: *Optional* - Whether the user is online in `bool` form.
        - ``relationship``: *Optional* - The `Relationship` of the user.
        - ``status``: *Optional* - The `Status` of the user.
        - ``flags``: *Optional* - The flags of the user in `int` form.
        - ``bot``: *Optional* - The `BotUser` object, if a user is a bot.

    .. method:: __repr__()
            
        Gets the string representation of the user.

        :returns: :class:`str`
            The string representation of the user.
            
            ``<pyrevolt.User id={self.userID} username={self.username} badges={self.badges} relationship={self.relationship} online={self.online} bot={self.bot}>``

    .. method:: __str__()

        Get the username of the user.

        :returns: :class:`str`
            The username of the user.

    .. method:: copy()

        Creates a copy of the user.

        :returns: :class:`User`
            The copy of the user.

    .. method:: update(updateData, clear)
            
        Updates the user with the data from the update data.

        :param updateData:
        :type updateData: :class:`dict`
            The update data.
        :param clear:
        :type clear: :class:`list[str]`
            Items to clear data from.
        :returns None:
            None

    .. property:: mention

        Returns a string format to mention the user.

        :type: :class:`str`

    .. staticmethod:: FromJSON(jsonData, session)
            
        *This method is a coroutine.*

        Creates a user from a JSON object.

        :param jsonData:
        :type jsonData: :class:`str|bytes`
            The JSON formatted string.
        :param session:
        :type session: :class:`Session`
            The session object.
        :returns: :class:`User`
            The user.

    .. staticmethod:: FromID(userID, session)

        *This method is a coroutine.*

        Get a user from a user ID. This will attempt to fetch from the cache first.

        :param userID:
        :type userID: :class:`str`
            The ID of the user.
        :param session:
        :type session: :class:`Session`
            The session object.
        :returns: :class:`User`
            The user.

    .. staticmethod:: AttemptParse(content, session)

        *This method is a coroutine.*

        Attempts to parse a user from a string.

        :param content:
        :type content: :class:`str`
            The string to parse.
        :param session:
        :type session: :class:`Session`
            The session object.
        :returns: :class:`User|bool`
            The user or False if there is no user in the content.

Channels
--------

ChannelType
^^^^^^^^^^^
.. class:: ChannelType
    
    Bases: :class:`enum.Enum`

    Values:
        - SavedMessages
        - DirectMessages
        - Group
        - TextChannel
        - VoiceChannel

Channel
^^^^^^^
.. class:: Channel(channelID, type, **kwargs)

    A channel with an associated type.

    :param channelID:
    :type channelID: :class:`str`
        The ID of the channel.
    :param type:
    :type type: :class:`ChannelType`
        The type of the channel.
    :param kwargs:
        - ``session``: *Optional* - A `Session` object.

    .. method:: update(updateData, clear)

        Updates the channel with the data from the update data.

        :param updateData:
        :type updateData: :class:`dict`
            The update data.
        :param clear:
        :type clear: :class:`list[str]`
            Items to clear data from.
        :returns None:
            None

    .. staticmethod:: FromJSON(jsonData, session)
                
        *This method is a coroutine.*

        Creates a channel from a JSON object.

        :param jsonData:
        :type jsonData: :class:`str|bytes`
            The JSON formatted string.
        :param session:
        :type session: :class:`Session`
            The session object.
        :returns: :class:`Channel`
            The channel.

    .. staticmethod:: FromID(channelID, session)
            
        *This method is a coroutine.*

        Get a channel from a channel ID. This will attempt to fetch from the cache first.

        :param channelID:
        :type channelID: :class:`str`
            The ID of the channel.
        :param session:
        :type session: :class:`Session`
            The session object.
        :returns: :class:`Channel`
            The channel.

    .. staticmethod:: AttemptParse(content, session)
            
        *This method is a coroutine.*

        Attempts to parse a channel from a string.

        :param content:
        :type content: :class:`str`
            The string to parse.
        :param session:
        :type session: :class:`Session`
            The session object.
        :returns: :class:`Channel|bool`
            The channel or False if there is no channel in the content.

    .. method:: Send(**kwargs)

        Sends a message to the channel.

        :param kwargs:
        :type kwargs: :class:`dict`
            The message data.
        :returns None:
            None

SavedMessages
^^^^^^^^^^^^^
.. class:: SavedMessages(channelID, user, **kwargs)

    Bases: :class:`Channel`

    A saved messages channel.

    :param channelID:
    :type channelID: :class:`str`
        The ID of the channel.
    :param user:
    :type user: :class:`User`
        The user the saved messages are with.
    :param kwargs:
        - ``session``: *Optional* - Parameters to pass to `Channel`.

    .. method:: __repr__()
            
        Gets the string representation of the channel.

        :returns: :class:`str`
            The string representation of the channel.
            
            ``<pyrevolt.SavedMessages id={self.channelID} user={self.user}>``

    .. method:: copy()

        Creates a copy of the channel.

        :returns: :class:`SavedMessages`
            The copy of the channel.    

DirectMessage
^^^^^^^^^^^^^
.. class:: DirectMessage(channelID, active, recipients, **kwargs)

    Bases: :class:`Channel`

    A direct message channel.

    :param channelID:
    :type channelID: :class:`str`
        The ID of the channel.
    :param active:
    :type active: :class:`bool`
        Whether the direct message is active or not.
    :param recipients:
    :type recipients: :class:`list[User]`
        The users the direct message is with.
    :param kwargs:
        - ``session``: *Optional* - `Session` to pass to `Channel` constructor.

    .. method:: __repr__()
            
        Gets the string representation of the channel.

        :returns: :class:`str`
            The string representation of the channel.
            
            ``<pyrevolt.DirectMessage id={self.channelID} active={self.active} recipients={self.recipients}>``

    .. method:: copy()

        Creates a copy of the channel.

        :returns: :class:`DirectMessage`
            The copy of the channel.

Group
^^^^^
.. class:: Group(channelID, name, recipients, owner, **kwargs)

    Bases: :class:`Channel`

    A group channel.

    :param channelID:
    :type channelID: :class:`str`
        The ID of the channel.
    :param name:
    :type name: :class:`str`
        The name of the group.
    :param recipients:
    :type recipients: :class:`list[User]`
        The users the group is with.
    :param owner:
    :type owner: :class:`User`
        The owner of the group.
    :param kwargs:
        - ``session``: *Optional* - `Session` to pass to `Channel` constructor.
        - ``description``: *Optional* - The description in `str` form for the group.
        - ``lastMessageID``: *Optional* - The `str` ID of the last message in the group.
        - ``permissions``: *Optional* - The permissions in `int` form for the group.
        - ``nsfw``: *Optional* - A `bool` the group is NSFW or not.

    .. method:: __repr__()
                
        Gets the string representation of the channel.

        :returns: :class:`str`
            The string representation of the channel.
            
            ``<pyrevolt.Group id={self.channelID} name={self.name} recipients={self.recipients} owner={self.owner}>``

    .. method:: __str__()

        Get the name of the group.

        :returns: :class:`str`
            The name of the group.

    .. method:: copy()

        Creates a copy of the channel.

        :returns: :class:`Group`
            The copy of the channel.

ServerChannel
^^^^^^^^^^^^^
.. class:: ServerChannel(channelID, type, server, name, **kwargs)
    
    Bases: :class:`Channel`

    A server channel.

    :param channelID:
    :type channelID: :class:`str`
        The ID of the channel.
    :param type:
    :type type: :class:`ChannelType`
        The type of the channel.
    :param server:
    :type server: :class:`Server`
        The server the channel is in.
    :param name:
    :type name: :class:`str`
        The name of the channel.
    :param kwargs:
        - ``session``: *Optional* - `Session` to pass to `Channel` constructor.
        - ``description``: *Optional* - The description in `str` form for the channel.
        - ``defaultPermissions``: *Optional* - The default permissions in `int` form for the channel.
        - ``nsfw``: *Optional* - A `bool` the channel is NSFW or not.

    .. method:: __str__()

        Get the name of the channel.

        :returns: :class:`str`
            The name of the channel.

TextChannel
^^^^^^^^^^^
.. class:: TextChannel(channelID, server, name, **kwargs)
    
    Bases: :class:`ServerChannel`

    A text channel.

    :param channelID:
    :type channelID: :class:`str`
        The ID of the channel.
    :param server:
    :type server: :class:`Server`
        The server the channel is in.
    :param name:
    :type name: :class:`str`
        The name of the channel.
    :param kwargs:
        - ``session``: *Optional* - `Session` to pass to `ServerChannel` constructor.
        - ``description``: *Optional* - The description in `str` form for the channel.
        - ``defaultPermissions``: *Optional* - The default permissions in `int` form for the channel.
        - ``nsfw``: *Optional* - A `bool` the channel is NSFW or not.
        - ``lastMessageID``: *Optional* - The `str` ID of the last message in the channel.

    .. method:: __repr__()
                
        Gets the string representation of the channel.

        :returns: :class:`str`
            The string representation of the channel.
            
            ``<pyrevolt.TextChannel id={self.channelID} server={self.server.serverID} name={self.name}>``

    .. method:: copy()

        Creates a copy of the channel.

        :returns: :class:`TextChannel`
            The copy of the channel.

VoiceChannel
^^^^^^^^^^^^
.. class:: VoiceChannel(channelID, server, name, **kwargs)
    
    Bases: :class:`ServerChannel`

    A voice channel.

    :param channelID:
    :type channelID: :class:`str`
        The ID of the channel.
    :param server:
    :type server: :class:`Server`
        The server the channel is in.
    :param name:
    :type name: :class:`str`
        The name of the channel.
    :param kwargs:
        - ``session``: *Optional* - `Session` to pass to `ServerChannel` constructor.
        - ``description``: *Optional* - The description in `str` form for the channel.
        - ``defaultPermissions``: *Optional* - The default permissions in `int` form for the channel.
        - ``nsfw``: *Optional* - A `bool` the channel is NSFW or not.

    .. method:: __repr__()
                
        Gets the string representation of the channel.

        :returns: :class:`str`
            The string representation of the channel.
            
            ``<pyrevolt.VoiceChannel id={self.channelID} server={self.server.serverID} name={self.name}>``

    .. method:: copy()

        Creates a copy of the channel.

        :returns: :class:`VoiceChannel`
            The copy of the channel.

Messages
--------

EmbedType
^^^^^^^^^
.. class:: EmbedType
    
    Bases: :class:`enum.Enum`

    Values:
        - Website
        - Image
        - Text

EmbedImageSize
^^^^^^^^^^^^^^
.. class:: EmbedImageSize
    
    Bases: :class:`enum.Enum`

    Values:
        - Large
        - Preview

Embed
^^^^^
.. class:: Embed(type, **kwargs)

    An embed in a message.

    :param type:
    :type type: :class:`EmbedType`
        The type of the embed.
    :param kwargs:
        - ``url`` - *Optional* - The URL in `str` form for the embed (*Required* for `EmbedType.Image`).
        - ``specials`` - *Optional* - A `dict` of special embed types, only applicable to `EmbedType.Website`.
        - ``title`` - *Optional* - The title in `str` form for the embed.
        - ``description`` - *Optional* - The description in `str` form for the embed.
        - ``siteName`` - *Optional* - The site name in `str` form for the embed.
        - ``iconURL`` - *Optional* - The icon URL in `str` form for the embed.
        - ``colour`` - *Optional* - The colour in `str` form (``#xxxxxx``) for the embed.
        - ``width`` - *Required for `EmbedType.Image`* - The width in `int` form for the embed.
        - ``height`` - *Required for `EmbedType.Image`* - The height in `int` form for the embed.
        - ``size`` - *Required for `EmbedType.Image`* - The size in `EmbedImageSize` form for the embed.

    .. method:: __repr__()
        
        Gets the string representation of the embed.

        :returns: :class:`str`
            The string representation of the embed.
            
            ``<pyrevolt.Embed type={self.type}>``

    .. method:: toJSON()
            
        Gets the JSON representation of the embed.

        :returns: :class:`str`
            The JSON representation of the embed.

    .. staticmethod:: FromJSON(jsonData)

        Creates an embed from the JSON representation.

        :param json:
        :type json: :class:`str|bytes`
            The JSON representation of the embed.
        :returns: :class:`Embed`
            The embed.

    .. staticmethod:: Create(**kwargs)

        Create a Text embed from the specified kwargs

        :param kwargs:
            - ``iconURL``: *Optional* - The icon URL in `str` form for the embed.
            - ``url``: *Optional* - The URL in `str` form for the embed.
            - ``title``: *Optional* - The title in `str` form for the embed.
            - ``description``: *Optional* - The description in `str` form for the embed.
            - ``colour``: *Optional* - The colour in `str` form (``#xxxxxx``) for the embed.

Masquerade
^^^^^^^^^^
.. class:: Masquerade(**kwargs)

    Masquerade with a different avatar and/or name.

    :param kwargs:
        - ``avatar``: *Optional* - The avatar URL in `str` form for the masquerade.
        - ``name``: *Optional* - The name in `str` form for the masquerade.
    :returns: :class:`Masquerade`
        The masquerade.

    .. staticmethod:: FromJSON(jsonData)
    
        Creates a masquerade from the JSON representation.

        :param json:
        :type json: :class:`str|bytes`
            The JSON representation of the masquerade.
        :returns: :class:`Masquerade`
            The masquerade.

Reply
^^^^^
.. class:: Reply(messageID, mention)

    A reply to a message.

    :param messageID:
    :type messageID: :class:`str`
        The ID of the message.
    :param mention:
    :type mention: :class:`str`
        The mention in `str` form for the reply.
    :returns: :class:`Reply`
        The reply.

    .. staticmethod:: FromJSON(jsonData)
    
        Creates a reply from the JSON representation.

        :param json:
        :type json: :class:`str|bytes`
            The JSON representation of the reply.
        :returns: :class:`Reply`
            The reply.

Message
^^^^^^^
.. class:: Message(messageID, channel, author, **kwargs)

    A message.

    :param messageID:
    :type messageID: :class:`str`
        The ID of the message.
    :param channel:
    :type channel: :class:`Channel`
        The channel the message is in.
    :param author:
    :type author: :class:`User`
        The author of the message.
    :param kwargs:
        - ``content``: *Optional* - The `str` content for the message.
        - ``nonce`` - *Optional* - The nonce (number used once) in `str` form for the message.
        - ``edited`` - *Optional* - The time the message was edited in `datetime` form.
        - ``embeds`` - *Optional* - A `list` of embeds in `Embed` form for the message.
        - ``mentions`` - *Optional* - A `list` of mentions in `User` form for the message.
        - ``replies`` - *Optional* - A `list` of replies in `Reply` form for the message.
        - ``masquerade`` - *Optional* - The masquerade in `Masquerade` form for the message.
        - ``session`` - *Optional* - The `Session` to cache the message.

    .. method:: __repr__()
        
        Gets the string representation of the message.

        :returns: :class:`str`
            The string representation of the message.
            
            ``<pyrevolt.Message id={self.messageID} channel={self.channel} author={self.author}>``

    .. method:: copy()
        
        Gets a copy of the message.

        :returns: :class:`Message`
            The copy of the message.

    .. method:: update(updatedData)

        *This method is a coroutine.*

        Updates the message with the specified data.

        :param updatedData:
        :type updatedData: :class:`dict`
            The updated data.
        :returns None:
            None.

    .. property:: url

        The URL of the message in `str` form.

        :type: :class:`str`
    
    .. staticmethod:: FromJSON(jsonData, session)
    
        *This method is a coroutine.*

        Creates a message from the JSON representation.

        :param json:
        :type json: :class:`str|bytes`
            The JSON representation of the message.
        :param session:
        :type session: :class:`Session`
            The session to cache the message.
        :returns: :class:`Message`
            The message.

    .. staticmethod:: FromID(channelID, messageID, session)

        *This method is a coroutine.*

        Gets a message from the specified channel and ID. If the message is not cached, it will be fetched from the API.

        :param channelID:
        :type channelID: :class:`str`
            The ID of the channel.
        :param messageID:
        :type messageID: :class:`str`
            The ID of the message.
        :param session:
        :type session: :class:`Session`
            The session to cache the message.
        :returns: :class:`Message`
            The message.

    .. staticmethod:: generateMessageData(**kwargs)
        
        *This method is a coroutine.*

        Generates a dictionary with the message data for the given kwargs.

        :param kwargs:
            - ``content``: *Optional* - The content in `str` form for the message.
            - ``replies``: *Optional* - A `list` of replies in `Reply` form for the message.
            - ``embed``: *Optional* - An `Embed` to attach with the message.
            - ``embeds``: *Optional* - A `list` of embeds in `Embed` form for the message.
            - ``masquerade``: *Optional* - The  `Masquerade` of which to alter the bot to.

    .. method:: Send(**kwargs)

        *This method is a coroutine.*

        Sends the message.

        :param kwargs:
            - ``content``: *Optional* - The content in `str` form for the message.
            - ``replies``: *Optional* - A `list` of replies in `Reply` form for the message.
            - ``embed``: *Optional* - An `Embed` to attach with the message.
            - ``embeds``: *Optional* - A `list` of embeds in `Embed` form for the message.
            - ``masquerade``: *Optional* - The  `Masquerade` of which to alter the bot to.
        :returns: :class:`Message`
            The sent message.

    .. staticmethod:: Create(channel, **kwargs)

        *This method is a coroutine.*

        Creates a message.

        :param channel:
        :type channel: :class:`Channel`
            The channel to create the message in.
        :param kwargs:
            - ``content``: *Optional* - The content in `str` form for the message.
            - ``replies``: *Optional* - A `list` of replies in `Reply` form for the message.
            - ``embed``: *Optional* - An `Embed` to attach with the message.
            - ``embeds``: *Optional* - A `list` of embeds in `Embed` form for the message.
            - ``masquerade``: *Optional* - The  `Masquerade` of which to alter the bot to.
        :returns: :class:`Message`
            The created message.

Server
------

Category
^^^^^^^^
.. class:: Category(categoryID, title, channels)

    A category holds multiple channels in a server.

    :param categoryID:
    :type categoryID: :class:`str`
        The ID of the category.
    :param title:
    :type title: :class:`str`
        The title of the category.
    :param channels:
    :type channels: :class:`list[ServerChannel]`
        The channels in the category.
    :return None:
        None.

    .. method:: __repr__()
        
        Gets the string representation of the category.

        :returns: :class:`str`
            The string representation of the category.
            
            ``<pyrevolt.Category id={self.categoryID} title={self.title} channels={self.channels}>``

    .. staticmethod:: FromJSON(jsonData, session)
        
        *This method is a coroutine.*

        Creates a category from the JSON representation.

        :param json:
        :type json: :class:`str|bytes`
            The JSON representation of the category.
        :param session:
        :type session: :class:`Session`
            The session to cache the category.
        :returns: :class:`Category`
            The category.

SystemMessages
^^^^^^^^^^^^^^
.. class:: SystemMessages(**kwargs)

    A object to hold which channels get sent system messages for the server.

    :param kwargs:
        - ``userJoinedChannel``: *Optional* - The `ServerChannel` that user join messages are sent to.
        - ``userLeftChannel``: *Optional* - The `ServerChannel` that user leave messages are sent to.
        - ``userKickedChannel``: *Optional* - The `ServerChannel` that user kick messages are sent to.
        - ``userBannedChannel``: *Optional* - The `ServerChannel` that user ban messages are sent to.

    .. method:: __repr__()

        Gets the string representation of the system messages.

        :returns: :class:`str`
            The string representation of the system messages.
            
            ``<pyrevolt.SystemMessages userJoinedChannel={self.userJoinedChannel} userLeftChannel={self.userLeftChannel} userKickedChannel={self.userKickedChannel} userBannedChannel={self.userBannedChannel}>``

    .. staticmethod:: FromJSON(jsonData, session)
        
        *This method is a coroutine.*

        Creates a system messages from the JSON representation.

        :param json:
        :type json: :class:`str|bytes`
            The JSON representation of the system messages.
        :param session:
        :type session: :class:`Session`
            The session to cache the system messages.
        :returns: :class:`SystemMessages`
            The system messages.

Role
^^^^
.. class:: Role(roleID, name, permissions, **kwargs)

    A role in a server.

    :param roleID:
    :type roleID: :class:`str`
        The ID of the role.
    :param name:
    :type name: :class:`str`
        The name of the role.
    :param permissions:
        The permissions of the role.
    :param kwargs:
        - ``colour``: *Optional* - The colour of the role.
        - ``hoist``: *Optional* - Whether the role is hoisted.
        - ``rank``: *Optional* - The rank of the role.

    .. method:: __repr__()

        Gets the string representation of the role.

        :returns: :class:`str`
            The string representation of the role.
            
            ``<pyrevolt.Role id={self.roleID} name={self.name} permissions={self.permissions} colour={self.colour} hoist={self.hoist} rank={self.rank}>``

    .. method:: update(updatedData, clear)
        
        *This method is a coroutine.*

        Updates the role.

        :param updatedData:
        :type updatedData: :class:`dict`
            The updated data for the role.
        :param clear:
        :type clear: :class:`list[str]`
            The keys to clear from the role.
        :return None:
            None.

    .. staticmethod:: FromJSON(jsonData)
        
        *This method is a coroutine.*

        Creates a role from the JSON representation.

        :param json:
        :type json: :class:`str|bytes`
            The JSON representation of the role.
        :returns: :class:`Role`
            The role.

Server
^^^^^^
.. class:: Server(serverID, owner, name, channels, defaultPermissions, **kwargs)

    A server.

    :param serverID:
    :type serverID: :class:`str`
        The ID of the server.
    :param owner:
    :type owner: :class:`User`
        The owner of the server.
    :param name:
    :type name: :class:`str`
        The name of the server.
    :param channels:
    :type channels: :class:`list[ServerChannel]`
        The channels in the server.
    :param defaultPermissions:
        The default permissions of the server.
    :param kwargs:
        - ``description``: *Optional* - The `str` description of the server.
        - ``categories``: *Optional* - The `list` of `Category` in the server.
        - ``systemMessages``: *Optional* - The `SystemMessages` of the server.
        - ``roles``: *Optional* - The `list` of `Role` in the server.
        - ``nsfw``: *Optional* - Whether the server is nsfw.
        - ``flags``: *Optional* - The `int` flags of the server.
        - ``analytics``: *Optional* - Whether analytics are being collected from the server
        - ``discoverable``: *Optional* - Whether the server is discoverable.

    .. method:: __repr__()

        Gets the string representation of the server.

        :returns: :class:`str`
            The string representation of the server.
            
            ``<pyrevolt.Server id={self.serverID} owner={self.owner} name={self.name} channels={self.channels} defaultPermissions={self.defaultPermissions}>``

    .. method:: copy()

        Copies the server.

        :returns: :class:`Server`
            The server.

    .. method:: update(updatedData, clear)

        *This method is a coroutine.*

        Updates the server.

        :param updatedData:
        :type updatedData: :class:`dict`
            The updated data for the server.
        :param clear:
        :type clear: :class:`list[str]`
            The keys to clear from the server.
        :return None:
            None.

    .. staticmethod:: FromJSON(jsonData, session)

        *This method is a coroutine.*

        Creates a server from the JSON representation.

        :param json:
        :type json: :class:`str|bytes`
            The JSON representation of the server.
        :param session:
        :type session: :class:`Session`
            The session to cache the server.
        :returns: :class:`Server`
            The server.

    .. staticmethod:: FromID(serverID, session)

        *This method is a coroutine.*

        Gets the server from the ID.

        :param serverID:
        :type serverID: :class:`str`
            The ID of the server.
        :param session:
        :type session: :class:`Session`
            The session to cache the server.
        :returns: :class:`Server`
            The server.

Member
------
.. class:: Member(user, server, **kwargs)

    A member of a server.

    :param user:
    :type user: :class:`User`
        The user of the member.
    :param server:
    :type server: :class:`Server`
        The server of the member.
    :param kwargs:
        - ``nickname``: *Optional* - The nickname of the member.
        - ``roles``: *Optional* - The `list` of `Role` of the member.

    .. method:: __repr__()

        Gets the string representation of the member.

        :returns: :class:`str`
            The string representation of the member.
            
            ``<pyrevolt.Member id={self.memberID} user={self.user} server={self.server} nickname={self.nickname} roles={self.roles}>``

    .. method:: __str__()

        Get the members username

        :returns: :class:`str`
            The username of the member.

    .. property:: memberID

        The ID of the member.

        :type: :class:`str`

    .. method:: copy()

        Copies the member.

        :returns: :class:`Member`
            The member.

    .. method:: update(updatedData, clear)

        *This method is a coroutine.*

        Updates the member.

        :param updatedData:
        :type updatedData: :class:`dict`
            The updated data for the member.
        :param clear:
        :type clear: :class:`list[str]`
            The keys to clear from the member.

    .. staticmethod:: FromJSON(jsonData, session)

        *This method is a coroutine.*

        Creates a member from the JSON representation.

        :param json:
        :type json: :class:`str|bytes`
            The JSON representation of the member.
        :param session:
        :type session: :class:`Session`
            The session to cache the member.
        :returns: :class:`Member`
            The member.

    .. staticmethod:: FromID(memberID, session)

        *This method is a coroutine.*

        Gets the member from the ID.

        :param memberID:
        :type memberID: :class:`str`
            The ID of the member.
        :param session:
        :type session: :class:`Session`
            The session to cache the member.
        :returns: :class:`Member`
            The member.

Session
~~~~~~~

.. class:: Session()

    A session which manages and handles the `HTTPClient` and `Gateway` objects.

    :returns: :class:`Session`
        The session object.

    .. method:: Connect()

        *This method is a coroutine.*

        Connect the `Gateway`.

        :returns None:
            None

    .. method:: Start(token)

        *This method is a coroutine.*

        Starts the `Gateway` and `HTTPClient`.

        :param token:
        :type token: :class:`str`
            The bot token.
        :returns None:
            None

    .. method:: Close()

        *This method is a coroutine.*

        Closes the `Gateway` and `HTTPClient`.

        :returns None:
            None

    .. method:: Request(method, url, **kwargs)

        *This method is a coroutine.*

        Sends a request through the `HTTPClient`.

        :param method:
        :type method: :class:`Method`
            The HTTP method to use when sending the request.
        :param url:
        :type url: :class:`str`
            The URL to send the request to.
        :param kwargs:
            The keyword arguments to pass to the `HTTPClient`.
        :returns: :class:`dict`
            The JSON response from the server.

    .. method:: ProcessGateway(data)

        *This method is a coroutine.*

        Processes a gateway payload and dispatches the event.

        :param data:
        :type data: :class:`dict`
            The payload to process.
        :returns: :class:`dict`
            None

    .. method:: GatewayReceive()

        *This method is a coroutine.*

        Receives a gateway payload and executes `ProcessGateway`.

        :returns: :class:`dict`
            The payload received from the gateway.

    .. method:: GetUser(userID)

        *This method is a coroutine.*

        Gets a user from the cache. If the user is not present in the cache, it will be fetched
        from the API.

        :param userID:
        :type userID: :class:`str`
            The user ID to get information from.
        :returns: :class:`User`
            The user object.

    .. method:: GetChannel(channelID)
            
        *This method is a coroutine.*

        Gets a channel from the cache. If the channel is not present in the cache, it will be
        fetched from the API.

        :param channelID:
        :type channelID: :class:`str`
            The channel ID to get information from.
        :returns: :class:`Channel`
            The channel object.

    .. method:: GetServer(serverID)

        *This method is a coroutine.*

        Gets a server from the cache. If the server is not present in the cache, it will be
        fetched from the API.

        :param serverID:
        :type serverID: :class:`str`
            The server ID to get information from.
        :returns: :class:`Server`
            The server object.

    .. method:: GetRole(roleID)
            
        *This method is a coroutine.*

        Gets a role from the cache. If the role is not present in the cache, it will be fetched
        from the API.

        :param roleID:
        :type roleID: :class:`str`
            The role ID to get information from.
        :returns: :class:`Role`
            The role object.

    .. method:: GetMember(serverID, userID)

        *This method is a coroutine.*

        Gets a member from the cache. If the member is not present in the cache, it will be
        fetched from the API.

        :param serverID:
        :type serverID: :class:`str`
            The server ID to get information from.
        :param userID:
        :type userID: :class:`str`
            The user ID to get information from.
        :returns: :class:`Member`
            The member object.

Bot
~~~

.. class:: Bot(**kwargs)

    Represents a Bot and its connection to Revolt. Most interaction will be
    performed through this object at the highest abstraction level.

    :param kwargs:
        - ``prefix``: *Optional* - The prefix to use for all commands. (Default to blank `str`)
    :return Bot:
        A Bot object.

    .. class:: Commands(bot, **kwargs)

        A class contained by the Bot object responsible for registering and handling commands
        and errors that occur during command execution.

        :param bot:
        :type bot: :class:`Bot`
            The Bot object that this Commands object is associated with.
        :param kwargs:
            - ``prefix``: *Optional* - The prefix to use for all commands. (Default to blank `str`)
        :return Commands:
            A Commands object.

        .. decorator:: Command(**kwargs)

            Register a command for the given command. The command will be registered with the given ``kwargs``

            :params kwargs:
                - ``name``: *Required* - The name of the command.
                - ``aliases``: *Optional* - A list of aliases for the command. (Default to blank `list`)
            :return callable:
                A decorator that registers the given command.

        .. decorator:: Error(**kwargs)

            Register an error handler for the given command. The error handler will be registered to the command function
            it is called by.

            :params kwargs:
                - ``name``: *Required* - The name of the function to receive the errors from.
            :return callable:
                A decorator that registers the given error handler.

        .. method:: dispatchCommand(context)

            *This method is a coroutine.*

            Dispatches the given command to the appropriate functions.

            :param context:
            :type context: :class:`Message`
                The context of the command.
            :return None:
                None

    .. attribute:: commands

        The `Commands` object associated with this `Bot`.

        :type: :class:`Commands`

    .. method:: Start(**kwargs)

        *This method is a coroutine.*

        Asynchronously starts the bot. This method will block the current thread
        until the bot has been stopped in order to receive gateway information.

        :param kwargs:
            - ``token``: The bot's token.
        :return None:
            None.

    .. method:: Run(**kwargs)

        Runs the `Bot.Start()` function asynchronously.

        :param kwargs:
            - ``token``: The bot's token.
        :return None:
            None.

    .. decorator:: on(event)
        
        Registers a callback for a given event.

        :param event:
        :type event: :class:`GatewayEvent`
            The event to register the callback for.
        :return callable:
            The callback function.

    .. method:: GetUser(userID)

        *This method is a coroutine.*

        Asynchronously gets a user from the bot.

        :param userID:
        :type userID: :class:`str`
            The user's ID.
        :return User:
            The user.

    .. method:: GetChannel(channelID)

        *This method is a coroutine.*

        Asynchronously gets a channel from the bot.

        :param channelID:
        :type channelID: :class:`str`
            The channel's ID.
        :return Channel:
            The channel.

    .. method:: GetServer(serverID)

        *This method is a coroutine.*

        Asynchronously gets a server from the bot.

        :param serverID:
        :type serverID: :class:`str`
            The server's ID.
        :return Server:
            The server.

    .. method:: GetMember(memberID)

        *This method is a coroutine.*

        Asynchronously gets a member from the bot.

        :param memberID:
        :type memberID: :class:`str`
            The member's ID.
        :return Member:
            The member.

    .. method:: GetRole(serverID, roleID)

        *This method is a coroutine.*

        Asynchronously gets a role from the bot.

        :param serverID:
        :type serverID: :class:`str`
            The server's ID.
        :param roleID:
        :type roleID: :class:`str`
            The role's ID.
        :return Role:
            The role.