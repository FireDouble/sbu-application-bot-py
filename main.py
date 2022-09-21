import os
import random

import discord
import discord.utils
from discord.ext import commands

from dotenv import load_dotenv

from utils.setup import run_setup
from utils.constants import ADMIN_ID

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="+", intents=intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f"{bot.user} is ready")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
    print("All cogs loaded successfully")

@bot.command()
@commands.has_role(ADMIN_ID)
async def load_all(ctx: discord.ext.commands.Context):
    for filename in os.listdir('./cogs'):
        if not filename.endswith('.py'):
            continue

        bot.load_extension(f'cogs.{filename[:-3]}')

    await ctx.reply('Cogs loaded successfully')


@bot.command()
@commands.has_role(ADMIN_ID)
async def load(ctx: discord.ext.commands.Context, extension):
    try:
        bot.load_extension(f'cogs.{extension}')
    except discord.ExtensionAlreadyLoaded:
        await ctx.reply(f'Cog {extension} already loaded')
    except discord.ExtensionNotFound:
        await ctx.reply(f'Cog {extension} does not exist')
    else:
        await ctx.reply(f'Cog {extension} loaded successfully')


@bot.command()
@commands.has_role(ADMIN_ID)
async def unload(ctx, extension):
    try:
        bot.unload_extension(f'cogs.{extension}')
    except discord.ExtensionNotLoaded:
        await ctx.reply(f'Cog {extension} has not been loaded')
    except discord.ExtensionNotFound:
        await ctx.reply(f'Cog {extension} does not exist')
    else:
        await ctx.reply(f'Cog {extension} unloaded successfully')


@bot.command()
@commands.has_role(ADMIN_ID)
async def reload(ctx):
    for filename1 in os.listdir('./cogs'):
        if not filename1.endswith('.py'):
            continue

        try:
            bot.unload_extension(f'cogs.{filename1[:-3]}')
        except discord.ExtensionNotLoaded:
            print(f'Cog {filename1[:-3]} has not been loaded')

    for filename1 in os.listdir('./cogs'):
        if not filename1.endswith('.py'):
            continue

        bot.load_extension(f'cogs.{filename1[:-3]}')

    await ctx.reply('Cogs reloaded successfully')

if __name__ == '__main__':
    run_setup()
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
    