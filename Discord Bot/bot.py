import os
import random
import requests
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

# intents = discord.Intents.default()
# intents.message_content = True
# client = discord.Client(intents=intents)


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
    # get the bot's username and stop when you find a hashtag
    username = str(message.author).split('#')[0]
    # in the discord's Username
    user_message = str(message.content)  # the content of the message
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    # make sure the chatbot does not indefinitely respond to its own message
    if message.author == client.user:
        return  # don't do anything

    # check if the channel is the right one (i.e. make sure it does not respond to any channel)
    if message.channel.name == 'general':
        print("inside general")
        # add a message that the bot should recognize before responding
        print(f'{username}: {user_message} ({channel})')
        if user_message.lower() == 'hello':
            await message.channel.send(f'Hey {message.author.mention}!!')
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
        # if this word is contained in any part of the message, then delete the whole message.
        elif 'fuck' in message.content:
            await message.channel.send(
                f'Hey😠 {message.author.mention},😠 Profanity is not allowed on this server😠😠😠')
            await message.delete()
            return

        # create a message than can be responded anywhere on the server
        if user_message.lower() == '!anywhere':
            await message.channel.send('This can be used anywhere')
            return

        # check what time is it. when "what time" is typed, no matter what follows, respond
        if 'what time' in user_message.lower():
            time = datetime.now().strftime('%H:%M:%S')
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
            voice_client = message.guild.voice_client

            if voice_client and voice_client.is_connected():
                await voice_client.move_to(channel)
            else:
                await channel.connect()
                message.guild.voice_client.mute = False  # Unmute the bot when it joins the voice channel

        if message.content.startswith('!leave'):
            voice_client = message.guild.voice_client

            if voice_client and voice_client.is_connected():
                await voice_client.disconnect()

        if message.content.startswith('!games') and message.author.guild.voice_client is not None:
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
                'outtmpl': 'games.mp3',
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
            embed.set_image(url=res['data']['children']
                            [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)


# run the program
client.run(TOKEN)
