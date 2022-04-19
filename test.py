from src import pyrevolt

@pyrevolt.OnMessage()
async def onMessage(channel: pyrevolt.Channel, author: pyrevolt.User, content: str) -> None:
    print(f"{author.userID} in {channel.channelID}: {content}")
    if content == "!ping":
        await channel.Send(f"Pong! <@{author.userID}>")

bot = pyrevolt.Bot()
bot.run(token="yThS2_GNBdir55tRj5tzfWQZH8-8c-k0ia1vpyJiWiSv8ymsssxNC9wis9_v3kM0")