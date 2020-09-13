import discord
from discord.ext import commands
import datetime
import mysql.connector
from data import settings


class ManualSetup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def resetall(self, ctx):
        guild = ctx.guild.id
        db_counting = mysql.connector.connect(host=settings.host, user=settings.user, passwd=settings.passwd,
                                              database=settings.database)
        counting_cursor = db_counting.cursor()

        counting_cursor.execute(f"SELECT * FROM counting_guildsettings WHERE guild_id = {guild}")
        result = counting_cursor.fetchone()

        if result[1] != 0:
            counting_cursor.execute(f"UPDATE counting_guildsettings SET counting_channel_id = 0 WHERE guild_id = {guild}")
            counting_cursor.execute(f"UPDATE counting_guildsettings SET maxcount = 2147483647 WHERE guild_id = {guild}")
            counting_cursor.execute(f"UPDATE counting_guildsettings SET restart_on_error = 0 WHERE guild_id = {guild}")
            counting_cursor.execute(f"UPDATE counting_guildsettings SET emote_react = 0 WHERE guild_id = {guild}")
            counting_cursor.execute(f"UPDATE counting_guildsettings SET toggle = 0 WHERE guild_id = {guild}")
            db_counting.commit()

            counting_cursor.execute(f"UPDATE counting_data SET number = 0 WHERE guild_id = {guild}")
            counting_cursor.execute(f"UPDATE counting_data SET last_user_id = 0 WHERE guild_id = {guild}")
            counting_cursor.execute(f"DELETE FROM counting_userdata WHERE guild_id = {guild}")
            db_counting.commit()

            embed = discord.Embed(
                description=f"**Reset Complete!** Do `c!setup` to activate the bot again!",
                color=settings.embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
        else:
            embed = discord.Embed(
                description=f"**Reset Failed!** No setup was done!",
                color=settings.embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=settings.footer)
        await ctx.send(embed=embed)
        db_counting.close()

    @resetall.error
    async def resetall_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("You don't have enough permissions. "
                           "You need to have the **OWNER** of this Guild to use this command.")


def setup(client):
    client.add_cog(ManualSetup(client))
