import discord
from discord.ext import commands
import mysql.connector
from data import settings


class ToggleCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def toggle(self, ctx):
        guild = ctx.guild.id
        db_counting = mysql.connector.connect(host=settings.host, user=settings.user, passwd=settings.passwd,
                                              database=settings.database)
        counting_cursor = db_counting.cursor()

        counting_cursor.execute(f"SELECT * FROM counting_guildsettings WHERE guild_id = {guild}")
        result_tuple = counting_cursor.fetchone()

        if result_tuple[5] == 0:
            number = 1
            word = "paused"
            other_word = "unpause"
        else:
            number = 0
            word = "unpaused"
            other_word = "pause"

        counting_cursor.execute(f"UPDATE counting_guildsettings SET toggle = {number} WHERE guild_id = {guild}")
        db_counting.commit()

        embed = discord.Embed(
            title="Counting Toggle",
            description=f"You have {word} the counting channel.\nType ` c!toggle ` to {other_word} the counting.",
            color=settings.embedcolor
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=settings.footer)
        await ctx.send(embed=embed)
        db_counting.close()

    @toggle.error
    async def toggle_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            return


def setup(client):
    client.add_cog(ToggleCmd(client))
