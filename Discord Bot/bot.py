import discord
import random
import os

from dotenv import load_dotenv
from datetime import datetime


# load the token from the .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')
# The unique token of the bot retrieved from Discord documentation (https://discord.com/developers/applications)

# create a client
client = discord.Client()

# path to read from
os.chdir("/Users/cuenc/Downloads")


# create a client event
@client.event
async def on_ready():  # once you start the bot, this async function is called
    print('Online Bot {0.user}'.format(client))


# Respond to user input commands
@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]  # get the bot's username and stop when you find a hashtag
    # in the discord's Username
    user_message = str(message.content)  # the content of the message
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel}')

    # make sure the chatbot does not indefinitely respond to its own message
    if message.author == client.user:
        return  # don't do anything

    # check if the channel is the right one (i.e. make sure it does not respond to any channel)
    if message.channel.name == 'general':
        # add a message that the bot should recognize before responding
        if user_message.lower() == 'hello' or user_message.lower() == 'hey' or user_message.lower() == 'hi':  # case insensitive
            await message.channel.send(f'Hello {username} :)!')  # respond to the username that sent the message
            return
        # similarly, we add more if statements
        elif user_message.lower() == 'ciao':
            await message.channel.send(f'Ci vediamo dopo!!')
            return
        elif user_message.lower() == '!random':
            response = f'This is your random number: {random.randrange(1000000)}'
            await message.channel.send(response)
            return
        elif user_message.lower() == 'γαμαθ':
            await message.channel.send(f'50 Euro')
            return
        # delete the message sent by the user if it contains profanity
        elif 'fuck' in message.content:  # if this word is contained in any part of the message, then delete the whole message.
            await message.channel.send(f'Hey😠 {message.author.mention},😠 Profanity is not allowed on this server😠😠😠')
            await message.delete()
            return

        # create a message than can be responded anywhere on the server
        if user_message.lower() == '!anywhere':
            await message.channel.send('This can be used anywhere')
            return

        if user_message.lower() == 'what time is it?':
            time = datetime.now()
            await message.channel.send(f'Hey {username} the time is:')
            await message.channel.send(time)
            return

        # the following statement uploads a picture (meme)
        if user_message.lower() == 'meme':
            with open('PointersMeme.jpg', 'r') as f:
                await message.channel.send(file=discord.File('/Users/cuenc/Downloads/PointersMeme.jpg'))


# Read the Bot Token from another file (which will not be public) and store that info in the TOKEN variable.
# Upd: better version in the top, using .env file
# with open('.env') as f:
#   TOKEN = f.readline()





# run the program
client.run(TOKEN)
