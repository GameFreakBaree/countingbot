import discord
from discord.ext import commands
import datetime
import mysql.connector
from data import settings


class UnlinkCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def link(self, ctx):
        guild = ctx.guild.id
        db_counting = mysql.connector.connect(host=settings.host, user=settings.user, passwd=settings.passwd,
                                              database=settings.database)
        counting_cursor = db_counting.cursor()

        counting_cursor.execute(f"SELECT * FROM counting_guildsettings WHERE guild_id = {guild}")
        result = counting_cursor.fetchone()

        if result[1] == 0:
            await ctx.channel.set_permissions(self.client.user, send_messages=True, read_messages=True,
                                              add_reactions=True, embed_links=True, manage_messages=True,
                                              read_message_history=True, external_emojis=True,
                                              manage_permissions=True)

            counting_cursor.execute(
                f"UPDATE counting_guildsettings SET counting_channel_id = {ctx.channel.id} WHERE guild_id = {guild}")
            db_counting.commit()

            embed = discord.Embed(
                description=f"**Link Complete!** You can now use the counting features!",
                color=settings.embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=settings.footer)
            await ctx.send(embed=embed)
        db_counting.close()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def unlink(self, ctx):
        guild = ctx.guild.id
        db_counting = mysql.connector.connect(host=settings.host, user=settings.user, passwd=settings.passwd,
                                              database=settings.database)
        counting_cursor = db_counting.cursor()

        counting_cursor.execute(f"SELECT * FROM counting_guildsettings WHERE guild_id = {guild}")
        result = counting_cursor.fetchone()

        if result[1] != 0:
            counting_cursor.execute(f"UPDATE counting_guildsettings SET counting_channel_id = 0 WHERE guild_id = {guild}")
            db_counting.commit()

            embed = discord.Embed(
                description=f"**Unlink Complete!** Do `c!link` to activate the bot again!",
                color=settings.embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=settings.footer)
            await ctx.send(embed=embed)
        db_counting.close()

    @link.error
    async def link_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have enough permissions. "
                           "You need to have the **MANAGE_SERVER** permission to use this command.")
        error = getattr(error, "original", error)
        if isinstance(error, discord.Forbidden):
            await ctx.send("The bot has not enough permissions. "
                           "Try giving the bot Administrator Permissions to run the setup command. "
                           "Then you can remove those permissions.\n"
                           "If you don't want that, just make sure the bot has the permission **Manage Permissions** in the counting channel.\n"
                           "After that, run the ` c!setup ` command in the same channel.")

    @unlink.error
    async def unlink_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have enough permissions. "
                           "You need to have the **MANAGE_SERVER** permission to use this command.")


def setup(client):
    client.add_cog(UnlinkCmd(client))
