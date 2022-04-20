<h1 align="center" style="font-size: 48px;">pyrevolt</h1>
<div align="center">
A Python library to wrap the Revolt API, made to be easy-to-use but powerful and feature rich.
</div>
<div align="center">

[![Version](https://img.shields.io/badge/version-0.1.4--a-red)](https://img.shields.io/badge/version-0.1.4--a-red) [![Stability](https://img.shields.io/badge/stability-Use%20if%20experienced-important)](https://img.shields.io/badge/stability-Use%20if%20experienced-important)
</div>

## Installing pyrevolt
**Python 3.10 or greater is required**

To install pyrevolt, you can run the following command:
```python
# Linux/macOS command
python3 -m pip install py   revolt
# Windows
py -m pip install pyrevolt
```

## Using pyrevolt
This shows a very quick example of how to use pyrevolt. As a note, pyrevolt is still under heavy development and this example and the library as a whole may change.
```py
import pyrevolt

bot = pyrevolt.Bot(prefix="!")

@pyrevolt.Ready()
async def onReady(users: list[pyrevolt.User], channels: list[pyrevolt.Channel], servers: list[pyrevolt.Server]) -> None:
    print("Ready!")

@bot.on(pyrevolt.GatewayEvent.OnMessage)
async def onMessage(message: pyrevolt.Message) -> None:
    print(f"{message.author.username} said: {message.content}")

@bot.commands.Command(name="ping")
async def ping(message: pyrevolt.Message) -> None:
    await message.Send(content=f"Pong {message.author.username}!", embeds=[pyrevolt.Embed.Create(title="Pong!", description=f"{message.author.mention}!", colour="#0000ff")], replies=[pyrevolt.Reply(message.messageID, True)])

@bot.commands.Command(name="hello", aliases=["hi"])
async def hello(message: pyrevolt.Message, name: str) -> None:
    await message.Send(content=f"Hello {name}!")
@hello.Error
async def helloError(message: pyrevolt.Message, error: Exception) -> None:
    await message.Send(content=f"{str(error)}")

bot.Run(token="TOKEN")
```

As the library expands, more examples will be added, but we expect users during the very initial development phases to read through the source in order to find how to develop (this will of course change over the development of the library).

### Useful Information
#### Code Quality
[![CodeFactor](https://www.codefactor.io/repository/github/genericnerd/pyrevolt/badge)](https://www.codefactor.io/repository/github/genericnerd/pyrevolt)
[![CircleCI](https://circleci.com/gh/GenericNerd/pyrevolt.svg?style=shield)](https://app.circleci.com/pipelines/github/GenericNerd/pyrevolt)
[![StyleCI](https://github.styleci.io/repos/471419418/shield?branch=production)](https://github.styleci.io/repos/471419418?branch=production)
#### Repository Information
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/GenericNerd/pyrevolt.svg)](http://isitmaintained.com/project/GenericNerd/pyrevolt "Percentage of issues still open")