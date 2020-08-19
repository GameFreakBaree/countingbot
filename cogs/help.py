import discord
from discord.ext import commands
import datetime
import mysql.connector
import json

with open('./db_settings.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

host = settings['host']
user = settings['user']
passwd = settings['passwd']
database = settings['database']

read_settings.close()

db_counting = mysql.connector.connect(
    host=host,
    database=database,
    user=user,
    passwd=passwd
)

counting_cursor = db_counting.cursor()
counting_cursor.execute("SELECT footer FROM counting_settings")
embed_footer = counting_cursor.fetchone()

counting_cursor.execute("SELECT embed_color FROM counting_settings")
embed_color_tuple = counting_cursor.fetchone()
embed_color = int(embed_color_tuple[0], 16)


class HelpMsg(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="help")
    async def helpcmd(self, ctx):
        prefix = ('c!',)
        owner = ctx.guild.owner

        if ctx.author == owner:
            embed = discord.Embed(
                description=f"**__Staff Commands__**\n"
                            f"\n• **{prefix[0]}autosetup** - Automatically sets up the channels for you."
                            f"\n• **{prefix[0]}setup** - Make the channel where you do this command into a counting channel."
                            f"\n• **{prefix[0]}reset** - Reset the bot and remove the channel as a counting channel."
                            f"\n• **{prefix[0]}config** - Configurate the bot however you like."
                            f"\n• **{prefix[0]}pause** - Pause the counting in the count channel. <:premium_only:742810459048116364> "
                            f"\n• **{prefix[0]}unpause** - Unpause the counting in the count channel. <:premium_only:742810459048116364> "
                            f"\n• **{prefix[0]}setcount <number>** - Set the count manually on a number. <:premium_only:742810459048116364> "
                            f"\n• **{prefix[0]}activate <key>** - Activate the premium bot. <:premium_only:742810459048116364> "
                            f"\n\n**__Member Commands__**\n"
                            f"\n• **{prefix[0]}help** - Displays this Embed."
                            f"\n• **{prefix[0]}ping** - Get the ping in milliseconds of the bot."
                            f"\n• **{prefix[0]}info** - Get all the information about the bot."
                            f"\n• **{prefix[0]}premium** - Get all information how to get the premium bot."
                            f"\n• **{prefix[0]}leaderboard** - Get a leaderboard with members that counted the most."
                            f"\n• **{prefix[0]}user** - See how many times you counted in the server.",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
        else:
            embed = discord.Embed(
                description=f"\n• **{prefix[0]}help** - Displays this Embed."
                            f"\n• **{prefix[0]}ping** - Get the ping in milliseconds of the bot."
                            f"\n• **{prefix[0]}info** - Get all the information about the bot."
                            f"\n• **{prefix[0]}premium** - Get all information how to get the premium bot."
                            f"\n• **{prefix[0]}leaderboard** - Get a leaderboard with members that counted the most."
                            f"\n• **{prefix[0]}user** - See how many times you counted in the server.",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=embed_footer[0])
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(HelpMsg(client))
