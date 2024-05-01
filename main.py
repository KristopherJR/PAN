import os
import discord
import pan
import requests

from dotenv import load_dotenv

async def process_message(message):
    try:
        bot_response = pan.handle_user_messages(message.content)
        if bot_response:
            await message.channel.send(bot_response)
    except Exception as error:
        print(error)

def run_bot():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv("DISCORD_GUILD")
    client = discord.Client(intents=discord.Intents.all())

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