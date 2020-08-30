import asyncio
import os
import discord
from discord.ext import commands
import json

with open('db_settings.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

token = settings['token']

read_settings.close()

client = commands.Bot(command_prefix='c!', case_insensitive=True)
client.remove_command("help")


async def change_status():
    await client.wait_until_ready()
    while client.is_ready():
        status = discord.Activity(name=f"c!help | {len(client.guilds)} Guilds", type=discord.ActivityType.playing)
        await client.change_presence(activity=status)
        await asyncio.sleep(60)


@client.event()
async def on_ready():
    print(f"[CountingBot] The bot is online and ready to use!")


@client.command()
async def load(ctx, extension):
    if ctx.author.id == 643072638075273248:
        client.load_extension(f'cogs.{extension}')
        print(f"Load {extension}, door {ctx.author}")
        await ctx.send(f"Load {extension}, succes!")


@client.command()
async def reload(ctx, extension):
    if ctx.author.id == 643072638075273248:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        print(f"Reload {extension}, door {ctx.author}")
        await ctx.send(f"Reload {extension}, succes!")


@client.command()
async def unload(ctx, extension):
    if ctx.author.id == 643072638075273248:
        client.unload_extension(f'cogs.{extension}')
        print(f"Unload {extension}, door {ctx.author}")
        await ctx.send(f"Unload {extension}, succes!")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        print(f"[CountingBot] Cogs > {filename[:-3]} > Loaded!")
        client.load_extension(f'cogs.{filename[:-3]}')

client.loop.create_task(change_status())
client.run(token)
