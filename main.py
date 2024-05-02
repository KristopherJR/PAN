import os
import pan
import requests
import discord
import nacl
from dotenv import load_dotenv
from discord.ext import commands
from discord import FFmpegPCMAudio

async def process_message(message):
    try:
        bot_response = await pan.handle_user_messages(message)
        if bot_response:
            await message.channel.send(bot_response)
    except Exception as error:
        print(error)

def run_bot():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv("DISCORD_GUILD")

    client = commands.Bot(command_prefix='.', intents=discord.Intents.all())
    voice = discord.VoiceChannel

    @client.event
    async def on_ready():
        guild = discord.utils.get(client.guilds, name=GUILD)

        print(
            f"{client.user} is connected to the following guild:\n"
            f"{guild.name}(id: {guild.id})"
        )

    @client.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(f"{member.name}... Need some Grog...")

    @client.event
    async def on_message(message):
        if (message.author == client.user):
            return
        await process_message(message)

    client.run(TOKEN)

run_bot()