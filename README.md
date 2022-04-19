<h1 align="center" style="font-size: 48px;">pyvolt</h1>
<div align="center">
A Python library to wrap the Revolt API, made to be easy-to-use but powerful and feature rich.
</div>
<div align="center">

[![Version](https://img.shields.io/badge/version-0.1.1--a-red)](https://img.shields.io/badge/version-0.1.1--a-red) [![Stability](https://img.shields.io/badge/stability-Use%20if%20experienced-important)](https://img.shields.io/badge/stability-Use%20if%20experienced-important)
</div>
## Installing pyvolt
**Python 3.10 or greater is required**
To install pyvolt, you can run the following command:
```python
# Linux/macOS command
python3 -m pip install pyvolt
# Windows
py -m pip install pyvolt
```

## Using pyvolt
This shows a very quick example of how to use pyvolt. As a note, pyvolt is still under heavy development and this example and the library as a whole may change.
```py
import pyvolt

@pyvolt.OnMessage()
async def onMessage(channel: pyvolt.Channel, author: pyvolt.User, content: str) -> None:
    print(f"{author.userID} in {channel.channelID}: {content}")
    if content == "!ping":
        await channel.Send(f"Pong! <@{author.userID}>")

bot = pyvolt.Bot()
bot.run(token="TOKEN")
```

As the library expands, more examples will be added, but we expect users during the very initial development phases to read through the source in order to find how to develop (this will of course change over the development of the library).

### Useful Information
#### Code Quality
[![CodeFactor](https://www.codefactor.io/repository/github/genericnerd/pyvolt/badge)](https://www.codefactor.io/repository/github/genericnerd/pyvolt)
[![CircleCI](https://circleci.com/gh/GenericNerd/pyvolt.svg?style=shield)](https://app.circleci.com/pipelines/github/GenericNerd/pyvolt)
[![StyleCI](https://github.styleci.io/repos/471419418/shield?branch=production)](https://github.styleci.io/repos/471419418?branch=production)
#### Repository Information
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/GenericNerd/pyvolt.svg)](http://isitmaintained.com/project/GenericNerd/pyvolt "Percentage of issues still open")