import os
import pan
import requests
import discord
import nacl
import asyncio
import random
from dotenv import load_dotenv
from discord import FFmpegPCMAudio

async def play_sfx(channel, sfx_path):
    vc = await channel.connect()
    print(f'Joined {channel.name}!')

    ffmpeg_options = {
        'executable': os.getenv("FFMPEG")
    }

    audio = discord.FFmpegPCMAudio(sfx_path, **ffmpeg_options)
    vc.play(audio)
    # Wait until the audio has finished playing
    while vc.is_playing():
        await asyncio.sleep(1)
    # Disconnect from the voice channel once the audio has finished playing
    await vc.disconnect()
    print(f'Disconnected from {channel.name}!')


def random_gragas_sfx() -> str:
    return f'audio/gragas-{random.randint(1,5)}.mp3'

async def handle_user_messages(msg) -> str:
    response = ""

    if validate_message(msg.content):
        message_parts = msg.content.split()
        command = message_parts[0]

        match command:
            case "/grog":
                channel = msg.author.voice.channel
                if channel:
                    await play_sfx(channel, random_gragas_sfx())
                else:
                    response = "Mmm... need some."
            case "/game":
                if len(message_parts) > 1:
                    summoner_name = msg.replace("/game ", "")
                    response = get_live_game(summoner_name)
                else:
                    response = "Give me a summoner name, bub."
    
    return response

def validate_message(msg) -> bool:
    return msg.count('/') == 1

def get_riot_api_token() -> str:
    return os.getenv("RIOT_API_TOKEN")

def get_live_game(summoner_name) -> str:
    puuid = get_puuid(summoner_name)
    token = get_riot_api_token()
    response = requests.get(f"https://euw1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}", headers={"X-Riot-Token": token})

    if (response.status_code == 404):
        return f"{summoner_name} is not currently in a game. What are you stupid?"
    if (response.status_code == 200):
        return response.content

def get_puuid(summoner_name) -> str:
    match summoner_name.lower():
        case "trinityburst":
            return "NawRoKFxfqWRCNvFRXSMDYGVaJQYsiLRpaNeIisdeMyy-3tJqS-YntU-zv15XVeoehmUVTEdtJfPCQ"
        case "somnus":
            return "3SkR0ZxsiB4mSK1sNt7lyHIdd_5gU0lVLxC3aJzsD9Ics7v7ijCGYU8v-yWwE289vZAM_gIE14y0wA"
        case "wheels":
            return "J_ZQ5LcyQ2bKPc0sdX0O7hZXLZBqiXO2pbrdjV6xAHW76oFBsHwAXSIwNqvSWf5--J2VS7aaTY7U7Q"
        case "smol keigo":
            return "J-PuAH8-ty3o1d_PrkDe4Ip8bY2lQmpndBr8dmAnLYdcg0C4wUtTCUMtKsixgUfsqn5PpBgdWrsebA"