import discord
import os
import youtube_dl
import asyncio
import urllib.request
import re

TOKEN = open('TOKEN.txt', 'r').read()

intents = discord.Intents.all()

client = discord.Client(intents=intents)

blocked_words = ["nigger", "tarbaby"]

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': '-vn'}


@client.event
async def on_ready():
    print("Testing bot logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}:{user_message}:({channel})')

    if message.author == client.user:
        return
    if message.content.lower() == 'ping':
        await message.channel.send('pong')
    if message.content.startswith('#hello'):
        await message.channel.send(f"Hello @{username} I am a still learning how to do thing around here\nLet me know "
                                   f"what you need")
    if message.content == '#private':
        await message.author.send("Why are you asking to speak to me in private. You are a bit sus mate")
    for word in blocked_words:
        if "Coder" not in str(message.author.roles) and word in str(message.content.lower()):
            await message.delete()
            await message.channel.send(
                f"{username} please refrain from using language like that in this discord server!")
            return
    ############
    if message.content.startswith("?playurl"):

        try:
            voice_client = await message.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("error")

        try:
            url = message.content.split()[1]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options,
                                            executable="C:\\Users\\JideO\\Downloads\\ezyZip\\ffmpeg-2022-08-29-git"
                                                       "-f99d15cca0-full_build\\bin\\ffmpeg.exe")

            voice_clients[message.guild.id].play(player)
            await message.channel.send(f"Now playing {url}")

        except Exception as err:
            print(err)
    if message.content.startswith("?play"):

        try:
            voice_client = await message.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("error")

        try:
            search_keyword = message.content[5:].replace(' ', '')
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            print("https://www.youtube.com/watch?v=" + video_ids[0])

            url = "https://www.youtube.com/watch?v=" + video_ids[0]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options,
                                            executable="C:\\Users\\JideO\\Downloads\\ezyZip\\ffmpeg-2022-08-29-git"
                                                       "-f99d15cca0-full_build\\bin\\ffmpeg.exe")

            voice_clients[message.guild.id].play(player)
            await message.channel.send(f"Now playing {url}")

        except Exception as err:
            print(err)

    if message.content.startswith("?pause"):
        try:
            voice_clients[message.guild.id].pause()
            await message.channel.send(f"Now paused")
        except Exception as err:
            print(err)

        # This resumes the current song playing if it's been paused
    if message.content.startswith("?resume"):
        try:
            voice_clients[message.guild.id].resume()
            await message.channel.send(f"Now resumed ")
        except Exception as err:
            print(err)

        # This stops the current playing song
    if message.content.startswith("?stop"):
        try:
            voice_clients[message.guild.id].stop()
            await voice_clients[message.guild.id].disconnect()
            await message.channel.send("safe you man")
        except Exception as err:
            print(err)


client.run(TOKEN)
