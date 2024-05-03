import discord
import os
import nacl
import asyncio
import random
# from discord import FFmpegPCMAudio

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