import discord
from discord.ext import commands
import helper as h

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
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
                    print(self.bot.voice_clients)


            elif before.channel is not None and after.channel is None:
                # The target user left a voice channel
                if self.bot.voice_clients:
                    # Disconnect the bot from the voice channel if it's connected
                    await self.bot.voice_clients[0].disconnect()


    def owner_status(self):
        owner_id = 244542391111909377
        guild_id = 943928163241717820
        guild = self.bot.get_guild(guild_id)
        owner = guild.get_member(owner_id)
        if owner.status == "online":
            return True
        else:
            return False


    @commands.Cog.listener()
    async def on_ready(self):
        # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for /dex "))
        await self.bot.load_extension("dex")
        # await bot.load_extension("tts") # package compatibility issue on linux (pedalboard)
        print(f"{h.timestamp()} Bot Activated")
        await self.bot.change_presence(status=discord.Status.offline)
        if self.owner_status(self):
            print(f"{h.timestamp()} Owner online, starting in online status")
            await self.bot.change_presence(status=discord.Status.online)
        else:
            print(f"{h.timestamp()} Owner offline, starting in offline status")
            await self.bot.change_presence(status=discord.Status.offline)

        await self.bot.tree.sync()


    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        if before.id == 244542391111909377:
            if str(before.status) == "online" and str(after.status) == "offline":
                print(f"{h.timestamp()} Bot going offline")
                await self.bot.change_presence(status=discord.Status.offline)
            elif str(before.status) == "offline" and str(after.status) == "online":
                print(f"{h.timestamp()} Bot going online")
                await self.bot.change_presence(status=discord.Status.online)

async def setup(bot):
    await bot.add_cog(Events(bot))