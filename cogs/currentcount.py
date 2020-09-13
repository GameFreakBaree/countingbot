import discord
from discord.ext import commands
import datetime
from data import settings
import mysql.connector


class CurrentCount(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def currentcount(self, ctx):
        guild = ctx.guild.id
        db_counting = mysql.connector.connect(host=settings.host, user=settings.user, passwd=settings.passwd,
                                              database=settings.database)
        counting_cursor = db_counting.cursor()

        counting_cursor.execute(
            f"SELECT number FROM counting_data WHERE guild_id = {guild}")
        number = counting_cursor.fetchone()

        embed = discord.Embed(
            title=f"Current Count",
            description=f"The Current count is: {number[0]}",
            color=settings.embedcolor,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=settings.footer)
        await ctx.send(embed=embed)
        db_counting.close()


def setup(client):
    client.add_cog(CurrentCount(client))
