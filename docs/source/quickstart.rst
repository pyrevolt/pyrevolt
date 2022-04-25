Quick Start
===========

.. _installation:

Installation
------------

pyrevolt only works with Python 3.10 or higher. Support for older versions of
Python is not provided.

You can get pyrevolt directly from PyPI:

If you are on Linux, you can install pyrevolt with:
.. code-block:: console
    $ python3 -m pip install -U pyrevolt

If you are on Windows, you can install pyrevolt with:
.. code-block:: console
    $ py -m pip install -U pyrevolt

Quick Start
-----------

In this section, we will make a bot that will respond to a specific command.

The code can look similar to this:
.. code-block:: python
    import pyrevolt

    bot: pyrevolt.Bot = pyrevolt.Bot(prefix="!")

    @bot.commands.Command(name="hello")
    async def hello(message: pyrevolt.Message) -> None:
        await message.Send("Hello!")

    bot.Run(token="TOKEN")

We will now break the code down line by line:
1. The first line import pyrevolt. If this raises a ``ModuleNotFoundError``, you
   probably don't have the latest version of pyrevolt installed.
2. The second line creates a new instance of the ``Bot`` class. This is our
   connection to pyrevolt. The ``prefix`` argument is the command prefix.
3. The third line decorates the next function as a command handler with the
   ``@bot.commands.Command`` decorator. This decorator takes a ``name`` argument
   which is the name of the command.
4. The fourth line creates a new function called ``hello``. This function will be
   called when the bot receives a message with the ``hello`` command, prefixed by ``!``.
5. The fifth line sends a message to the channel the message was received in with
   the content ``Hello!``.
6. The sixth line runs the bot using the token provided.

The bot can then be executed through the command line.

On Linux:
.. code-block:: console
    $ python3 exampleBot.py

On Windows:
.. code-block:: console
    $ py exampleBot.py