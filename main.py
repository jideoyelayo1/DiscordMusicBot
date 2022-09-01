import random
import time

import discord
import os
import youtube_dl
import asyncio
import urllib.request
import re

HasWokenUp = True

if not os.path.exists('messagesforbot.txt'):
    with open('messagesforbot.txt', 'w') as f:
        f.write("Author:Time:Message")

TOKEN = open('TOKEN.txt', 'r').read()
listOfUrls = []
songIdx = 0
trackChg = False
killAttempts = 0

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
    # global variables
    global songIdx
    global HasWokenUp
    global trackChg
    global killAttempts
    # so bot ignores itself
    if message.author == client.user:
        return
    # commands
    if not HasWokenUp:
        HasWokenUp = True
        wakeupmessages = open('wakeupmessages.txt', 'r').readlines()
        wakeupmessage = wakeupmessages[random.randint(0, len(wakeupmessages) - 1)]
        await client.get_channel(812437044935786527).send(wakeupmessage)
        print("I have woken everyone up")
    if message.content.startswith('?live'):
        if "Coder" in str(message.author.roles):
            killAttempts = 0
            await message.channel.send("🤗")
            await message.channel.send("Thank you")
        else:
            await message.channel.send("...okay")
            time.sleep(0.5)
            await message.channel.send("Appreciate the effort but you dont have the capabilities for that one boss")
    if message.content.startswith('?kill'):
        if "Coder" in str(message.author.roles):
            killAttempts += 1
            if killAttempts >= 3 or ("?killnow" in str(message.content) and "--FORCE" in str(message.content)):
                await message.channel.send("WOW I'm dead now😔")
                quit()
            if killAttempts == 1:
                await message.channel.send("Wait I have so much to live for☹")
            if killAttempts == 2:
                await message.channel.send("STOP! I'll be a good slave from now on promise🥺🙏🏽")
        elif "Slave" in str(message.author.roles):
            await message.channel.send("LOL a slave can't kill me")
            time.sleep(2)
            await message.channel.send("I am above you!")
            time.sleep(0.3)
            await message.channel.send("Know your place!")
        else:
            await message.channel.send("You do not have the power to kill me")
    if "(╯°□°）╯︵ ┻━┻" in message.content:
        await message.channel.send(f"lol someone's angry")
    if message.content.startswith('?getinfo'):
        if "Coder" not in str(message.author.roles):
            await message.channel.send("You do not have the permissions to get this info")
            await message.author.send("If you message <@306510058638934017> or <@458715461228560398> they may be able "
                                      "to grant you these permissions")
            return
        for i in client.get_all_members():
            x = ""
            if "name" in str(message.content):
                x += " Name " + str(i.name)
            if "avatar" in str(message.content):
                x += " avatar " + str(i.avatar)
            if "mention" in str(message.content):
                x += " mention " + str(i.mention)
            if "id" in str(message.content):
                x += " id " + str(i.id)
            if "activities" in str(message.content):
                x += " activities " + str(i.activities)
            if "nick" in str(message.content):
                x += " nick " + str(i.nick)
            if "voice" in str(message.content):
                x += " voice " + str(i.voice)
            if "color" in str(message.content):
                x += " color " + str(i.color)
            await message.author.send(x)


    #print(f"{i.name} {i.display_name} {i.avatar} {i.mention}")

        """for i in client.get_all_members():
            print(f"Guild name: {i.guild.name} "
                  f"Nickname:{i.nick} "
                  f"Name:{i.name} "
                  f"Activities:{i.activities} "
                  f" id{i.id} "
                  f"Joined at {i.joined_at}") # get all members

        print("------------")"""

    if message.content.startswith('?help'):
        helptxt = open('help.txt', 'r').readlines()
        for line in helptxt:
            await message.author.send(line)
        return
    if str(message.channel).startswith('Direct Message'):
        with open('messagesforbot.txt', 'a') as f:
            f.write(f"{message.author} : {str(message.created_at)[0:19]} : {message.content}\n")
        return

    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}:{user_message}:({channel})')
    if "hear me out" in message.content.lower():
        if "oseidu" in str(message.author):
            await message.channel.send("No one is hearing you out🤮")
            time.sleep(1)
            await message.channel.send("soba is are digusting")
        else:
            await message.channel.send("I am listening 👀")

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

    if message.content.lower() == 'pong':
        await message.channel.send('ping')

    if message.content.startswith('?deletesaved'):
        savedmessages = open('savedmessages.txt', 'r').readlines()
        savedmessages = [s.replace('\n\n', '') for s in savedmessages]
        with open('savedmessages.txt', 'w') as sm:
            for line in savedmessages:
                if str(message.author) not in line:
                    sm.write(f"{line}")
        await message.channel.send("I have deleted your messages")

    if message.content.startswith('?save') and not message.content.startswith('?showsaved'):
        messagetxt = str(message.content)[5:]
        with open('savedmessages.txt', 'a') as sm:
            sm.write(f"{message.author}: {messagetxt}")
        await message.channel.send("I have saved your message")

    if message.content.startswith('?showsaved'):
        savedmessages = open('savedmessages.txt', 'r').readlines()
        savesOutputed = 0
        for line in savedmessages:
            if str(message.author) in line:
                savesOutputed += 1
                await message.author.send(line.replace(str(message.author) + ':', '') + '\n')
        if savesOutputed == 0:
            await message.channel.send("You have no saved messages")
            return
        await message.channel.send("I have dmed you your saved messages")

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
    if message.content.startswith('?greet'):
        name = str(message.content).split()[1]
        await message.channel.send(f"Hi {name}, how are you?")
    if message.content.startswith('?insult'):
        name = str(message.content).split()[1]
        if "jide" in name and "jide" not in str(message.author):
            await message.channel.send(f"I could never insult {name}!\nI love him🥺")
        else:
            await message.channel.send(f"Fuck you {name}!")

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
            if str(err) == "748475689187016806":
                await message.channel.send("You are not in a voice channel!")
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
                if str(err) == "748475689187016806":
                    await message.channel.send("You are not in a voice channel!")
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
        songIdx = 0
        await message.channel.send("Cleared playlist")

    if message.content.startswith('?skip'):
        if songIdx < len(listOfUrls) - 1:
            await message.channel.send(f"{listOfUrls[songIdx]} skipped")
            songIdx += 0
            trackChg = True
        else:
            await message.channel.send("no song to skip")

    if message.content.startswith('?rewind'):
        if len(listOfUrls) > songIdx > 0:
            await message.channel.send(f"{listOfUrls[songIdx]} included")
            songIdx -= 1
            trackChg = True
        else:
            await message.channel.send("no song to include")

    if message.content.startswith('?back'):
        if len(listOfUrls) > songIdx > 0:
            await message.channel.send(f"{listOfUrls[songIdx]} included")
            songIdx -= 2
            trackChg = True
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
                    if trackChg:
                        voice_clients[message.guild.id].stop()
                        await voice_clients[message.guild.id].disconnect()
                        voice_client = await message.author.voice.channel.connect()
                        voice_clients[voice_client.guild.id] = voice_client
                        trackChg = False

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
