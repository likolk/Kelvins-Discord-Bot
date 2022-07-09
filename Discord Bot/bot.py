import discord
import random

# The unique token of the bot retrieved from Discord documentation (https://discord.com/developers/applications)
TOKEN = 'OTk1MjYxNTY0ODc1NzE0NjAy.GK40hd.MLVR7MVyHCYaipTQjyQscNrI0kDa8etuxBmC0w'

# create a client
client = discord.Client()


# create a client event
@client.event
async def on_ready(): # once you start the bot, this async function is called
    print('Online Bot {0.user}'.format(client))

if __name__ == "__main__":
    client.run(TOKEN)
# Run
