# bot.py
import os
import discord

TOKEN = 'DISCORD_TOKEN'

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
