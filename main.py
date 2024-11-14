import discord
from discord.ext import commands  # ^^^ all 2 essential
import os  # general-purpose
from dotenv import load_dotenv  # env file
import helper as h  # helper
from Commands import prepare_bot, get_bot_by_channel
from guppy import hpy  # resources monitor
import json
import ffmpeg

load_dotenv()  # load env file
TOKEN = os.getenv('DISCORD_TOKEN')  # load token from env
intents = discord.Intents.all()  # preparing all permissions for bot, mandatory
bot = commands.Bot(command_prefix="/", intents=intents)  # setting bot's prefix and permissions, mandatory


@bot.event
async def on_voice_state_update(member, before, after):
    # if before.channel is None and after.channel:
    #     channel = after.channel
    #     # print(member.id)
    #     # print(channel)
    #     json_file = open('intros.json')
    #     data = json.load(json_file)
    #     for row in data["intros_list"]:
    #         if str(member.id) == row['id'] and row['intro']:
    #             voice = await get_bot_by_channel(channel) # FIX BOT DISCONNECT PROBLEM
    #             voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source='intros/' + row['intro']))
    #     json_file.close()
    if member.id == int(244542391111909377):
        if before.channel is None and after.channel is not None:
            # The target user joined a voice channel
            target_channel = after.channel

            # Join the same channel
            try:
                vc = await target_channel.connect()
            except discord.errors.ClientException:
                print("error, already connected")
                print(bot.voice_clients)


        elif before.channel is not None and after.channel is None:
            # The target user left a voice channel
            if bot.voice_clients:
                # Disconnect the bot from the voice channel if it's connected
                await bot.voice_clients[0].disconnect()


def owner_status():
    owner_id = 244542391111909377
    guild_id = 943928163241717820
    guild = bot.get_guild(guild_id)
    owner = guild.get_member(owner_id)
    if owner.status == "online":
        return True
    else:
        return False


@bot.event
async def on_ready():
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for /dex "))
    await bot.load_extension("dex")
    # await bot.load_extension("tts") # package compatibility issue on linux (pedalboard)
    await bot.load_extension("Commands")
    print(f"{h.timestamp()} Bot Activated")
    await bot.change_presence(status=discord.Status.offline)
    if owner_status():
        print(f"{h.timestamp()} Owner online, starting in online status")
        await bot.change_presence(status=discord.Status.online)
    else:
        print(f"{h.timestamp()} Owner offline, starting in offline status")
        await bot.change_presence(status=discord.Status.offline)

    await bot.tree.sync()


@bot.event
async def on_presence_update(before, after):
    if before.id == 244542391111909377:
        if str(before.status) == "online" and str(after.status) == "offline":
            print(f"{h.timestamp()} Bot going offline")
            await bot.change_presence(status=discord.Status.offline)
        elif str(before.status) == "offline" and str(after.status) == "online":
            print(f"{h.timestamp()} Bot going online")
            await bot.change_presence(status=discord.Status.online)

@bot.command()
async def join(ctx):
    voice = await prepare_bot(ctx)

bot.run(TOKEN)


"""
@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def clock(ctx):
    await ctx.send(h.timestamp())

@bot.command()
async def joined(ctx, member: discord.Member):
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

@bot.group()
async def cool(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot(ctx):
    await ctx.send('Yes, the bot is cool.')

"""