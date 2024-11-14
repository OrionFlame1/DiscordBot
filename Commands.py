import time
import os
import discord as discord
from discord.ext import commands
import helper as h
from discord.utils import get
import yt_dlp as youtube_dl
import ffmpeg

start_time = time.time()

@commands.command()
async def imperial(ctx):
    if ctx.message.author.id == 244542391111909377:
        voice = await prepare_bot(ctx)
        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source='intros/imperial_march.m4a'))

@commands.command()
async def uptime(ctx):
    totaltime = time.time() - start_time
    print(f"Current uptime: {h.seconds_to_format(totaltime)}")
    await ctx.send(f"Uptime: {h.seconds_to_format(totaltime)}")

@commands.command()
async def setintro(ctx, *arg):
    if len(arg) == 0 or len(arg) > 1:
        await ctx.send(
            "```Use /setintro {link}```")
        return

@commands.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@commands.hybrid_command(
    name="play",
    description="Play a song"
)
async def play(ctx : commands.Context, *, query : str):
    time_start = time.time()
    voice = await prepare_bot(ctx)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'buffer',
        'default_search': 'auto',
    }

    try:
        os.remove("buffer.mp3")
    except:
        pass


    youtube_dl.YoutubeDL(ydl_opts).download(query)

    voice.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="buffer.mp3"))
    # voice.play()



    time_end = time.time()

    #
    # # ctx.voice_client.stop()
    # FFMPEG_OPTIONS = {
    #     'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    #     'options': '-vn',
    # }
    # ctx.voice_client.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))

@commands.command()
async def stop(ctx):
    await ctx.voice_client.stop()

@commands.command()
async def get_games(ctx):
    placeholder = await ctx.send("Fetching games, please wait...")
    epic = h.getEpicGames()
    message = ""
    for game in epic["games"]:
        if game["free_now"]:
            message += "**Free Now - [" + game["title"] + "](" + game["url"] + ")**\n"
        else:
            message += "[" + game["title"] + "](<" + game["url"] + ">)\n"
    await placeholder.edit(content=message)

async def prepare_bot(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(ctx.bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    return voice

async def get_bot_by_channel(channel):
    voice = await channel.connect()
    return voice

async def setup(bot):
    bot.add_command(imperial)
    bot.add_command(uptime)
    bot.add_command(setintro)
    bot.add_command(play)
    bot.add_command(stop)
    bot.add_command(leave)
    bot.add_command(get_games)
