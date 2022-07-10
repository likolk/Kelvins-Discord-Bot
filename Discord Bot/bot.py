import os
import random
from datetime import datetime

import aiohttp
import youtube_dl
from discord.ext.commands import Bot
from dotenv import load_dotenv
import discord
from discord.ext import commands
from requests import get
import json

bot = Bot(command_prefix='!')
intents = discord.Intents.default()
intents.members = True

# load the token from the .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')
# The unique token of the bot retrieved from Discord documentation (https://discord.com/developers/applications)


# create a client
# client = discord.Client()
client = commands.Bot(command_prefix="prefix")

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
        if user_message.lower() == 'hello' or user_message.lower() == 'hey' or user_message.lower() == 'hi':  # case
            # insensitive
            await message.channel.send(
                f'Hello {message.author.mention} :)!')  # respond to the username that sent the message
            return
        # similarly, we add more if statements
        elif user_message.lower() == 'ciao':
            await message.channel.send(f'Ci vediamo dopo{message.author.mention}!!')
            return
        elif user_message.lower() == '!random':
            response = f'{message.author.mention}This is your random number: {random.randrange(1000000)}'
            await message.channel.send(response)
            return
        elif user_message.lower() == 'γαμαθ':
            await message.channel.send(f'50 Euro {message.author.mention}')
            return
        # delete the message sent by the user if it contains profanity
        elif 'fuck' in message.content:  # if this word is contained in any part of the message, then delete the whole message.
            await message.channel.send(
                f'Hey😠 {message.author.mention},😠 Profanity is not allowed on this server😠😠😠')
            await message.delete()
            return

        # create a message than can be responded anywhere on the server
        if user_message.lower() == '!anywhere':
            await message.channel.send('This can be used anywhere')
            return

        if user_message.lower() == 'what time is it?':
            time = datetime.now()
            await message.channel.send(f'Hey {message.author.mention} the time is:')
            await message.channel.send(time)
            return

        # the following statement uploads a picture (meme)
        if user_message.lower() == 'haha':
            with open('PointersMeme.jpg', 'r') as f:
                await message.channel.send(f'Here is your meme {message.author.mention}')
                await message.channel.send(file=discord.File('/Users/cuenc/Downloads/PointersMeme.jpg'))

        # If user provides commands !join and !leave, the bot automatically joins/leaves the VC
        # NOTE: You need to have joined first the VC for this to work
        if message.content.startswith('!join'):
            channel = message.author.voice.channel
            await channel.connect()

        # leave vc
        if message.content.startswith('!leave'):
            if message.author.guild.voice_client is None:  # if the bot is not in the channel
                await message.channel.send('I must be in the Voice Channel in order to leave from it, isnt that '
                                           'obvious?😂😂')
            else:
                await message.channel.send('Disconnecting from the Voice Channel')
                await message.author.guild.voice_client.disconnect()

        # play a song #TODO: Currently not working properly
        if message.content.startswith('.play ') and message.author.guild.voice_client is not None:
            song = message.content[6:]
            if os.path.exists("games.mp3"):
                os.remove('games.mp3')
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': 'burak.mp3',
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([song])
            audio = discord.FFmpegPCMAudio('games.mp3')
            message.author.guild.voice_client.play(audio)
            await message.channel.send('Playing ' + song)


@bot.command()
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.add_roles(role)
    await ctx.send("role added")


@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)


# run the program
client.run(TOKEN)
