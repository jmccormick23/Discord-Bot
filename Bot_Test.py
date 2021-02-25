# bot.py
import os
import discord

TOKEN = 'ODExNjEwOTMyMjkxMzA1NTAy.YC0tlQ.F-mQK-eFLHwB4oU8V3srYgIMprs'

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
