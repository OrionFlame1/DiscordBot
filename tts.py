import pyttsx3
from pedalboard import Pedalboard, Chorus, Reverb, PitchShift, Compressor, Convolution
from pedalboard.io import AudioFile
import time
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from mutagen.mp3 import MP3

engine = pyttsx3.init()
engine.setProperty('volume', 1)
engine.setProperty('rate', 140)


def create_audio(name):
    engine.save_to_file(name, f'{name}.mp3')
    engine.runAndWait()

    # print(f"Name initially: {name}")

    with AudioFile(f'{name}.mp3') as f:
        audio = f.read(f.frames)
        samplerate = f.samplerate

    # Compressor(), Chorus(), Reverb(room_size=0.1), PitchShift(semitones=1),
    # Make a Pedalboard object, containing multiple plugins:
    board = Pedalboard([Compressor(), Chorus(), Reverb(room_size=0.1), PitchShift(semitones=1), Convolution(f"{name}.mp3", mix=0.1)])

    # Run the audio through this pedalboard!
    effected = board(audio, samplerate)

    with AudioFile(f'{name}.mp3', 'w', samplerate, effected.shape[0]) as f:
        f.write(effected)

    # print(f"expected output: {name}.mp3")

    # playsound(f'{name}.mp3')

    # print(f"--- {time.time() - start_time} seconds ---")


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


def get_username(ctx):
    if ctx.message.author.nick is not None:
        name = ctx.message.author.nick
    else:
        name = ctx.message.author.display_name
    return name


@commands.command()
async def hello(ctx):
    name = get_username(ctx)
    voice = await prepare_bot(ctx)
    create_audio("Hello " + name)
    source = FFmpegPCMAudio(f"Hello {name}.mp3")
    player = voice.play(source)
    audio = MP3(f"Hello {name}.mp3")
    time.sleep(int(audio.info.length) + 1)
    if os.path.exists(f"Hello {name}.mp3"):
        os.remove(f'Hello {name}.mp3')


@commands.command()
async def say(ctx, *arg):
    voice = await prepare_bot(ctx)
    sentence = " ".join(arg)
    create_audio(sentence)
    source = FFmpegPCMAudio(f"{sentence}.mp3")
    player = voice.play(source)
    audio = MP3(f"{sentence}.mp3")
    time.sleep(int(audio.info.length) + 1)
    if os.path.exists(f"{sentence}.mp3"):
        os.remove(f'{sentence}.mp3')


async def setup(bot):
    bot.add_command(hello)
    bot.add_command(say)

# say("Retrieving audio communication")
# say("Rogue Agent")
# print("")

# say(f"Disk usage at about {psutil.disk_usage('/').percent} percent")
