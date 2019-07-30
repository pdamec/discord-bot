import os
from settings import bot_prefix, discord_api_key
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=bot_prefix)

def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
        

if __name__ == "__main__":
    load_cogs()
    bot.run(discord_api_key)
