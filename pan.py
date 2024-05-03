import os
import discord
import league
import sound
import discord
from dotenv import load_dotenv
from discord.ext import commands

def run_bot():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv("DISCORD_GUILD")

    bot = commands.Bot(command_prefix='/',intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        guild = discord.utils.get(bot.guilds, name=GUILD)

        print(
            f"{bot.user} is connected to the following guild:\n"
            f"{guild.name}(id: {guild.id})"
        )

    @bot.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(f"{member.name}... Need some Grog...")

    @bot.event
    async def on_message(message):
        if (message.author == bot.user):
            return
        await process_message(message)

    bot.run(TOKEN)

async def process_message(message):
    try:
        bot_response = await handle_user_messages(message)
        if bot_response:
            await message.channel.send(bot_response)
    except Exception as error:
        print(error)

async def handle_user_messages(msg) -> str:
    response = ""

    if validate_message(msg.content):
        message_parts = msg.content.split()
        command = message_parts[0]

        match command:
            case "/grog":
                if msg.author.voice: #If the user that sent the command is in a voice channel
                    await sound.play_sfx(msg.author.voice.channel, sound.random_gragas_sfx())
                else:
                    response = "Mmm... need some."
            case "/game":
                if len(message_parts) > 1:
                    summoner_name = msg.content.replace("/game ", "")
                    response = league.get_live_game(summoner_name)
                else:
                    response = "Give me a summoner name, bub."
            case "/register":
                if len(message_parts) > 2:
                    tag = message_parts[-1]
                    summoner_name = " ".join(message_parts[1:][:-1])
                    response = league.register(summoner_name, tag)
                else:
                    response = "I'm gonna need your summoner name and tag, chief! `/register name tag`"

    return response

def validate_message(msg) -> bool:
    return msg.count('/') == 1

run_bot()