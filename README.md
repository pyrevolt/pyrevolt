<h1 align="center" style="font-size: 48px;">pyrevolt</h1>
<div align="center">
A Python library to wrap the Revolt API, made to be easy-to-use but powerful and feature rich.
</div>
<div align="center">

[![Version](https://img.shields.io/badge/version-0.2.7--a-red)](https://img.shields.io/badge/version-0.2.7--a-red) [![Stability](https://img.shields.io/badge/stability-Exceptions%20likely-yellowgreen)](https://img.shields.io/badge/stability-Exceptions%20likely-yellowgreen) [![Support Server](https://img.shields.io/badge/support-Revolt%20Server-informational)](https://app.revolt.chat/invite/mNygJpqw) [![Documentation Status](https://readthedocs.org/projects/pyrevolt/badge/?version=production)](https://pyrevolt.readthedocs.io/en/production/?badge=production)
</div>

## Installing pyrevolt
**Python 3.10 or greater is required**

To install pyrevolt, you can run the following command:
```python
# Linux/macOS command
python3 -m pip install pyrevolt
# Windows
py -m pip install pyrevolt
```

## Using pyrevolt
This shows a very quick example of how to use pyrevolt. As a note, pyrevolt is still under heavy development and this example and the library as a whole may change.
```py
import pyrevolt

bot = pyrevolt.Bot(prefix="!")

@pyrevolt.ReadySimplified()
async def onReady() -> None:
    print("Ready!")

@bot.on(pyrevolt.GatewayEvent.OnMessage)
async def onMessage(message: pyrevolt.Message) -> None:
    print(f"{message.author.username} said: {message.content}")

@bot.commands.Command(name="ping")
async def ping(message: pyrevolt.Message) -> None:
    await message.Send(content=f"Pong {message.author.username}!", embed=pyrevolt.Embed.Create(title="Pong!", description=f"{message.author.mention}!", colour="#0000ff"), replies=[pyrevolt.Reply(message.messageID, True)])

@bot.commands.Command(name="hello", aliases=["hi"])
async def hello(message: pyrevolt.Message, name: str) -> None:
    await message.Send(content=f"Hello {name}!")
@hello.Error
async def helloError(message: pyrevolt.Message, error: Exception) -> None:
    await message.Send(content=f"{str(error)}")

bot.Run(token="TOKEN")
```

As the library expands, more examples will be added, but we expect users during the very initial development phases to read through the documentation and see how to use the library. If you have any questions, please join the support server and ask for help.

### Useful Information
#### Code Quality
[![CodeFactor](https://www.codefactor.io/repository/github/pyrevolt/pyrevolt/badge)](https://www.codefactor.io/repository/github/pyrevolt/pyrevolt)
[![CircleCI](https://circleci.com/gh/pyrevolt/pyrevolt.svg?style=shield)](https://app.circleci.com/pipelines/github/pyrevolt/pyrevolt)
#### Repository Information
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/GenericNerd/pyrevolt.svg)](http://isitmaintained.com/project/GenericNerd/pyrevolt "Percentage of issues still open")
