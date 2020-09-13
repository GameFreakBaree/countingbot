import discord
from discord.ext import commands
import datetime
from data import settings

prefix = 'c!'


class HelpMsg(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="help")
    @commands.has_permissions(manage_guild=True)
    async def helpcmd(self, ctx):
        if ctx.author == ctx.guild.owner:
            embed = discord.Embed(
                description=f"**__Owner Commands__**\n"
                            f"\n• **{prefix}resetall** - Remove all data from the bot in the guild."
                            f"\n\n**__Staff Commands__**\n"
                            f"\n• **{prefix}autosetup** - Automatically sets up the channels for you."
                            f"\n• **{prefix}setup** - Make the channel where you do this command into a counting channel."
                            f"\n• **{prefix}unlink** - Run this command in the channel you want stop counting in."
                            f"\n• **{prefix}config** - Configurate the bot however you like."
                            f"\n• **{prefix}toggle** - Pause/Unpause the channel from counting in it."
                            f"\n• **{prefix}settopic** - Set the topic of the channel."
                            f"\n• **{prefix}resetscore <name>** - Reset a user's score."
                            f"\n\n**__Member Commands__**\n"
                            f"\n• **{prefix}help** - Displays this Embed."
                            f"\n• **{prefix}ping** - Get the ping in milliseconds of the bot."
                            f"\n• **{prefix}info** - Get all the information about the bot."
                            f"\n• **{prefix}invite** - Get an invite to add the bot."
                            f"\n• **{prefix}leaderboard** - Get a leaderboard with members that counted the most."
                            f"\n• **{prefix}userinfo <name>** - See how many times you counted in the server."
                            f"\n• **{prefix}currentcount** - Tells you on which number the count is.",
                color=settings.embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
        else:
            embed = discord.Embed(
                description=f"\n\n**__Staff Commands__**\n"
                            f"\n• **{prefix}autosetup** - Automatically sets up the channels for you."
                            f"\n• **{prefix}setup** - Make the channel where you do this command into a counting channel."
                            f"\n• **{prefix}unlink** - Run this command in the channel you want stop counting in."
                            f"\n• **{prefix}config** - Configurate the bot however you like."
                            f"\n• **{prefix}toggle** - Pause/Unpause the channel from counting in it."
                            f"\n• **{prefix}settopic** - Set the topic of the channel."
                            f"\n• **{prefix}resetscore <name>** - Reset a user's score."
                            f"\n\n**__Member Commands__**\n"
                            f"\n• **{prefix}help** - Displays this Embed."
                            f"\n• **{prefix}ping** - Get the ping in milliseconds of the bot."
                            f"\n• **{prefix}info** - Get all the information about the bot."
                            f"\n• **{prefix}invite** - Get an invite to add the bot."
                            f"\n• **{prefix}leaderboard** - Get a leaderboard with members that counted the most."
                            f"\n• **{prefix}userinfo <name>** - See how many times you counted in the server."
                            f"\n• **{prefix}currentcount** - Tells you on which number the count is.",
                color=settings.embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=settings.footer)
        await ctx.send(embed=embed)

    @helpcmd.error
    async def config_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"\n• **{prefix}help** - Displays this Embed."
                            f"\n• **{prefix}ping** - Get the ping in milliseconds of the bot."
                            f"\n• **{prefix}info** - Get all the information about the bot."
                            f"\n• **{prefix}invite** - Get an invite to add the bot."
                            f"\n• **{prefix}leaderboard** - Get a leaderboard with members that counted the most."
                            f"\n• **{prefix}userinfo <name>** - See how many times you counted in the server."
                            f"\n• **{prefix}currentcount** - Tells you on which number the count is.",
                color=settings.embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=settings.footer)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(HelpMsg(client))
