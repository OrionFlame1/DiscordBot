import datetime
from discord.ext import commands, tasks
import helper as h
import json
import traceback

eet = datetime.datetime.now().astimezone().tzinfo

time = datetime.time(hour=18, minute=1, tzinfo=eet)

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_games.start()

    def cog_unload(self):
        self.send_games.cancel()

    @tasks.loop(time=time)
    async def send_games(self):
        try:
            epic = h.getEpicGames()
            message = ""
            for game in epic["games"]:
                if game["free_now"]:
                    message += "**Free Now - [" + game["title"] + "](" + game["url"] + ")**\n"
                else:
                    message += "[" + game["title"] + "](<" + game["url"] + ">)\n"
            with open('subscribe.json', 'r') as file:
                data = json.load(file)
                for channel in data["channels"]:
                    chat_channel = self.bot.get_channel(int(channel["id"]))
                    placeholder = await chat_channel.send("Fetching games, please wait...")
                    await placeholder.edit(content=message)
        except Exception as e:
            traceback.print_exc()
            self.send_games(self)

    @send_games.before_loop
    async def before_send_games(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Tasks(bot))