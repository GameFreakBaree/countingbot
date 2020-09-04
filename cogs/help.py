import discord
from discord.ext import commands
import datetime
from data import settings


class HelpMsg(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="help")
    async def helpcmd(self, ctx):
        prefix = 'c!'
        if ctx.author == ctx.guild.owner:
            embed = discord.Embed(
                description=f"**__Staff Commands__**\n"
                            f"\n• **{prefix}autosetup** - Automatically sets up the channels for you."
                            f"\n• **{prefix}setup** - Make the channel where you do this command into a counting channel."
                            f"\n• **{prefix}reset** - Reset the bot and remove the channel as a counting channel."
                            f"\n• **{prefix}config** - Configurate the bot however you like."
                            f"\n• **{prefix}pause toggle** - (un)pause the counting in the count channel. <:premium_only:742810459048116364>"
                            f"\n• **{prefix}setcount <number>** - Set the count manually on a number. <:premium_only:742810459048116364>"
                            f"\n• **{prefix}activate <key>** - Activate the premium bot. <:premium_only:742810459048116364>"
                            f"\n\n**__Member Commands__**\n"
                            f"\n• **{prefix}help** - Displays this Embed."
                            f"\n• **{prefix}ping** - Get the ping in milliseconds of the bot."
                            f"\n• **{prefix}info** - Get all the information about the bot."
                            f"\n• **{prefix}premium** - Get all information how to get the premium bot."
                            f"\n• **{prefix}leaderboard** - Get a leaderboard with members that counted the most."
                            f"\n• **{prefix}user** - See how many times you counted in the server.",
                color=settings.embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
        else:
            embed = discord.Embed(
                description=f"\n• **{prefix}help** - Displays this Embed."
                            f"\n• **{prefix}ping** - Get the ping in milliseconds of the bot."
                            f"\n• **{prefix}info** - Get all the information about the bot."
                            f"\n• **{prefix}premium** - Get all information how to get the premium bot."
                            f"\n• **{prefix}leaderboard** - Get a leaderboard with members that counted the most."
                            f"\n• **{prefix}user** - See how many times you counted in the server.",
                color=settings.embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=settings.footer)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(HelpMsg(client))
