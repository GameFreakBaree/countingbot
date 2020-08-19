import discord
from discord.ext import commands


class OnReady(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        bot_naam = self.client.user.display_name
        print(f"[{bot_naam}] The bot is online and ready to use!")

        game = discord.Activity(name="c!help", type=discord.ActivityType.watching)
        await self.client.change_presence(activity=game)


def setup(client):
    client.add_cog(OnReady(client))
