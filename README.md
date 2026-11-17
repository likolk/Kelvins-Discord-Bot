# Kelvin's Discord Bot

A Discord bot written in Python with `discord.py`.

## What it does

- Replies to chat commands that start with `!`
- Joins and leaves voice channels with `!join` and `!leave`
- Plays audio in a voice channel
- Posts memes with the `meme` command
- Lets moderators mute a member with `!mute`

## Run it

```bash
pip install discord.py python-dotenv requests aiohttp youtube_dl
```

Create a `.env` file with your bot token as `TOKEN=...`, then:

```bash
python3 "Discord Bot/bot.py"
```

Never commit the `.env` file. It is listed in `.gitignore`.
