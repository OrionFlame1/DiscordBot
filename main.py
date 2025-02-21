import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()  # load env file
TOKEN = os.getenv('DISCORD_TOKEN')  # load token from env
intents = discord.Intents.all()  # preparing all permissions for bot, mandatory
bot = commands.Bot(command_prefix="/", intents=intents)  # setting bot's prefix and permissions, mandatory

async def load_cogs():
    for filename in os.listdir("./cogs"):  # Scan the 'cogs' folder
        if filename.endswith(".py"):  # Load Python files as extensions
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded cog: {filename}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())