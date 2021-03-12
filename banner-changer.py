import os
import random
import asyncio
import logging
import discord
from discord.ext import tasks, commands

guild_list = []
DELAY = {"hours":6, "minutes":0, "seconds":0}
BOT_TOKEN = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
IMG_PATH = "images"

logging.basicConfig(level=logging.INFO)

description = '''An icon changer bot'''
bot = commands.Bot(command_prefix='?', description=description)


@bot.event
async def on_guild_join():
    update_guild_list()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='with icons'))
    update_guild_list()
    print("logged in: ", bot.user)

async def update_guild_list():
    global guild_list
    guild_list = [g.id for g in bot.guilds]
    await create_guild_folders(guild_list)
    print("updated guild list")

async def create_guild_folders(guilds):
    for g in guilds:
        path = os.path.join(os.path.curdir, IMG_PATH, str(g.id))
        if(not os.path.exists(path)):
            os.makedirs(path)

@bot.command(description="Get the guild icon")
async def geticon(ctx):
    """Get the guild icon."""
    if ctx.message.guild is None:
        return
    await ctx.send(ctx.message.guild.icon_url)

async def set_random_icon_for_guild(guild_id):
    # https://stackoverflow.com/questions/701402/best-way-to-choose-a-random-file-from-a-directory
    image_path = random.choice([f for f in os.listdir(os.path.join(os.path.curdir, IMG_PATH, str(guild_id))) if os.path.isfile(os.path.join(os.path.curdir, IMG_PATH, str(guild_id), f))])
    image_path = os.path.join(os.path.curdir, IMG_PATH, str(guild_id), image_path)
    guild = bot.get_guild(guild_id)
    print("setting image:", image_path, guild_id)
    with open(image_path, 'rb') as data:
        try:
            await guild.edit(icon=data.read())
        except Exception as e:
            print(e)

@tasks.loop(**DELAY)
async def main():
    for guild in guild_list:
        await asyncio.sleep(random.randint(0, 10))
        try:
            await set_random_icon_for_guild(guild)
        except IOError as e:
            guild = bot.get_guild(guild)
            print(e, guild)


@main.before_loop
async def before_main():
    print("waiting for bot to become ready")
    await bot.wait_until_ready()


main.start()
bot.run(BOT_TOKEN)
