import random
import time

import discord
import os
import youtube_dl
import asyncio
import urllib.request
import re

TOKEN = open('TOKEN.txt', 'r').read()
listOfUrls = []
songIdx = 0

intents = discord.Intents.all()

client = discord.Client(intents=intents)

blocked_words = open('blocked_words.txt', 'r').readlines()

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': '-vn'}


@client.event
async def on_ready():
    print("Testing bot logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    global songIdx
    if message.author == client.user:
        return

    if message.content.startswith('?help'):
        helptxt = open('help.txt', 'r').readlines()
        for line in helptxt:
            await message.author.send(line)
        return

    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}:{user_message}:({channel})')

    if message.content.startswith('?random') or message.content.startswith('?odds'):
        try:
            num = int(message.content.split()[1])
            rnd = random.randint(0, num)
            await message.channel.send(f"picking a number from 0 to {num}")
            time.sleep(5)
            await message.channel.send(f'Computer has randomly picked {rnd}')
        except:
            if random.randint(0, 3) == 2 and "Slaves" in str(message.author.roles):
                await message.channel.send("Wait\n why is this slave speaking to me?")
            else:
                await message.channel.send("Invalid input")

    if message.content.lower() == 'ping':
        await message.channel.send('pong')
    if message.content.lower() == 'marco':
        await message.channel.send('polo')
    if message.content.startswith('?hello'):
        await message.channel.send(f"Hello @{username} I am a still learning how to do thing around here\nLet me know "
                                   f"what you need")
    if message.content == '?private':
        await message.author.send("Why are you asking to speak to me in private. You are a bit sus mate")
    for word in blocked_words:
        if "Coder" not in str(message.author.roles) and word in str(message.content.lower()):
            await message.delete()
            await message.channel.send(
                f"{username} please refrain from using language like that in this discord server!")
            return
    ############
    if message.content.startswith("?viewurls"):
        if not listOfUrls:
            await message.channel.send("List is empty")
            return
        await message.channel.send("List of urls:")
        for url in listOfUrls:
            await message.channel.send(url)
    if message.content.startswith("?deletelast"):
        if not listOfUrls:
            await message.channel.send("List is empty")
        else:
            del listOfUrls[-1]

    if message.content.startswith("?addurl"):
        listOfUrls.append(message.content.split()[1])
        await message.channel.send(f"{listOfUrls[-1]} has been added to the list")
    if message.content.startswith("?addsong"):
        try:
            search_keyword = message.content[5:].replace(' ', '')
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            print("https://www.youtube.com/watch?v=" + video_ids[0])

            listOfUrls.append("https://www.youtube.com/watch?v=" + video_ids[0])
            await message.channel.send(f"{listOfUrls[-1]} has been added to the list")
        except Exception as err:
            await message.channel.send(f"failed to add {listOfUrls[-1]}")
            print(err)

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
            await message.channel.send(f"{err}")
    if message.content.startswith("?play") and not message.content.startswith("?playurl"):
        playingSong = False
        tryCNT = 0
        while not playingSong:

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
                playingSong = True

            except Exception as err:
                ## stops an endless loop
                tryCNT += 1
                if tryCNT > 1:
                    break
                print(err)
                if str(err) == "Already playing audio.":
                    try:
                        voice_clients[message.guild.id].stop()
                        await voice_clients[message.guild.id].disconnect()
                        playingSong = False
                    except:
                        pass
                else:
                    await message.channel.send(f"{err}")
                    if str(err) == "Not connected to voice.":
                        break

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

    if message.content.startswith('?clear'):
        for i in range(songIdx):
            del listOfUrls[i]
        await message.channel.send("Cleared playlist")

    if message.content.startswith('?skip'):
        if songIdx < len(listOfUrls) - 1:
            await message.channel.send(f"{listOfUrls[songIdx]} skipped")
            songIdx += 1
        else:
            await message.channel.send("no song to skip")
    if message.content.startswith('?back'):
        if len(listOfUrls) > songIdx > 0:
            await message.channel.send(f"{listOfUrls[songIdx]} included")
            songIdx -= 1
        else:
            await message.channel.send("no song to include")
    if message.content.startswith('?resetIndex'):
        songIdx = 0
        await message.channel.send(f"index is {songIdx}")
    if message.content.startswith('?currentPlaylistSong'):
        try:
            await message.channel.send(listOfUrls[songIdx])
        except Exception as err:
            await message.channel.send("Can not display current song in playlist")
            print(err)
    if message.content.startswith('?stopplaylist'):
        looping = False
        songIdx = 0
        try:
            voice_clients[message.guild.id].stop()
            await voice_clients[message.guild.id].disconnect()
            await message.channel.send("safe you man")
        except Exception as err:
            print(err)

    if message.content.startswith('?startplaylist'):
        looping = True
        while looping and songIdx < len(listOfUrls):
            playingSong = False
            while not playingSong:

                try:
                    voice_client = await message.author.voice.channel.connect()
                    voice_clients[voice_client.guild.id] = voice_client
                except:
                    print("error")

                try:
                    url = listOfUrls[songIdx]
                    loop = asyncio.get_event_loop()
                    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

                    song = data['url']
                    player = discord.FFmpegPCMAudio(song, **ffmpeg_options,
                                                    executable="C:\\Users\\JideO\\Downloads\\ezyZip\\ffmpeg-2022-08-29-git"
                                                               "-f99d15cca0-full_build\\bin\\ffmpeg.exe")

                    voice_clients[message.guild.id].play(player)
                    await message.channel.send(f"Now playing {url}")
                    playingSong = True
                    songIdx += 1

                except Exception as err:
                    print(err)
                    if str(err) == "Already playing audio.":
                        pass
                    else:
                        print(err)
                        looping = False
                        break


client.run(TOKEN)
