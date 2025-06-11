import datetime
from discord.ext import commands, tasks
import json
import traceback
import os

import helper as h
import libs.checkFreeGames as checkFreeGames

eet = datetime.datetime.now().astimezone().tzinfo
time = datetime.time(hour=18, minute=1, tzinfo=eet)

class FreeEpicGamesNewsletter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_games.start()

    def cog_unload(self):
        self.send_games.cancel()

    def get_formatted_message(self):
        epic = checkFreeGames.getEpicGames()
        message = ""
        for game in epic:
            if game["free_now"]:
                message += "**Free Now - [" + game["title"] + "](" + game["url"] + ")**\n"
            else:
                message += "[" + game["title"] + "](<" + game["url"] + ">)\n"
        return message

    @commands.command()
    async def subscribe(self, ctx):
        if not os.path.exists('subscribe.json'):
            with open('subscribe.json', 'w') as file:
                json.dump({"channels": []}, file, indent=4)

        with open('subscribe.json', 'r') as file:
            data = json.load(file)
            for channel in data["channels"]:
                if str(ctx.channel.id) == channel["id"]:
                    await ctx.send("You are already subscribed to the Free Epic Games Newsletter.")
                    return
        with open('subscribe.json', 'r+') as file:
            data = json.load(file)
            data["channels"].append({"id": str(ctx.channel.id)})
            file.seek(0)
            json.dump(data, file, indent=4)
        await ctx.send("You have successfully subscribed to the Free Epic Games Newsletter.")

    @commands.command()
    async def unsubscribe(self, ctx):
        if not os.path.exists('subscribe.json'):
            await ctx.send("You are not subscribed to the Free Epic Games Newsletter.")
            return

        with open('subscribe.json', 'r') as file:
            data = json.load(file)
            for channel in data["channels"]:
                if str(ctx.channel.id) == channel["id"]:
                    data["channels"].remove(channel)
                    with open('subscribe.json', 'w') as file:
                        json.dump(data, file, indent=4)
                    await ctx.send("You have successfully unsubscribed from the Free Epic Games Newsletter.")
                    return
        await ctx.send("You are not subscribed to the Free Epic Games Newsletter.")

    @commands.command()
    async def get_games(self, ctx):
        placeholder = await ctx.send("Fetching games, please wait...")
        try:
            message = self.get_formatted_message()
            await placeholder.edit(content=message)
        except Exception as e:
            traceback.print_exc()
            await placeholder.edit(content="An error occurred while fetching the games. Please try again later.")
            return

    @tasks.loop(time=time)
    async def send_games(self):
        print(h.timestamp() + " Sending free Epic Games newsletter")
        try:
            message = self.get_formatted_message()
            with open('subscribe.json', 'r') as file:
                data = json.load(file)
                for channel in data["channels"]:
                    if os.path.exists('last_message.txt'):
                        with open('last_message.txt', 'r') as last_file:
                            last_message = last_file.read()
                        if message == last_message:
                            print(h.timestamp() + " No new games to send")
                            return
                    chat_channel = self.bot.get_channel(int(channel["id"]))
                    await chat_channel.send(message)
            with open('last_message.txt', 'w') as last_file:
                last_file.write(message)
        except Exception as e:
            traceback.print_exc()
            self.send_games(self)

    @send_games.before_loop
    async def before_send_games(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(FreeEpicGamesNewsletter(bot))