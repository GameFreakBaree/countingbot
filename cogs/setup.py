import discord
from discord.ext import commands
import datetime
import mysql.connector
from discord.ext.commands import MissingPermissions
from data import settings


class ManualSetup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx):
        guild = ctx.guild.id
        db_counting = mysql.connector.connect(host=settings.host, user=settings.user, passwd=settings.passwd,
                                              database=settings.database)
        counting_cursor = db_counting.cursor()

        counting_cursor.execute(f"SELECT * FROM counting_guildsettings WHERE guild_id = {guild}")
        result = counting_cursor.fetchall()
        result_tuple = result[0]
        if result_tuple[2] == 0:
            await ctx.channel.set_permissions(self.client.user, send_messages=True, read_messages=True,
                                              add_reactions=True, embed_links=True, manage_messages=True,
                                              read_message_history=True, external_emojis=True,
                                              manage_permissions=True)

            counting_cursor.execute(f"UPDATE counting_guildsettings SET counting_channel_id = {ctx.channel.id} WHERE guild_id = {guild}")
            db_counting.commit()

            embed = discord.Embed(
                description=f"**Setup Complete!** You can now use the counting features!\n"
                            f"\nIf the bot does not add emotes or delete false messages, please make sure that"
                            f"the bot has the permissions in the channel. Otherwise, give Administrator to the bot",
                color=settings.embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=settings.footer)
            await ctx.author.send(embed=embed)
        else:
            embed = discord.Embed(
                description=f"**Setup Failed!** You already did the setup command!",
                color=settings.embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=settings.footer)
            await ctx.author.send(embed=embed)
        db_counting.close()

    @commands.command()
    async def autosetup(self, ctx):
        guild = ctx.guild.id
        db_counting = mysql.connector.connect(host=settings.host, user=settings.user, passwd=settings.passwd,
                                              database=settings.database)
        counting_cursor = db_counting.cursor()

        counting_cursor.execute(f"SELECT * FROM counting_guildsettings WHERE guild_id = {guild}")
        result = counting_cursor.fetchall()
        result_tuple = result[0]
        if result_tuple[2] == 0:
            counting_channel = await ctx.guild.create_text_channel('counting')
            await counting_channel.set_permissions(self.client.user, send_messages=True, read_messages=True,
                                                   add_reactions=True, embed_links=True, manage_messages=True,
                                                   read_message_history=True, external_emojis=True,
                                                   manage_permissions=True)

            counting_cursor.execute(f"UPDATE counting_guildsettings SET counting_channel_id = {counting_channel.id} WHERE guild_id = {guild}")
            db_counting.commit()

            embed = discord.Embed(
                description=f"**Auto Setup Complete!** You can now use the counting features!",
                color=settings.embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=settings.footer)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description=f"**Auto Setup Failed!** You already did the setup command!",
                color=settings.embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=settings.footer)
            await ctx.send(embed=embed)
        db_counting.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx):
        guild = ctx.guild.id
        db_counting = mysql.connector.connect(host=settings.host, user=settings.user, passwd=settings.passwd,
                                              database=settings.database)
        counting_cursor = db_counting.cursor()

        counting_cursor.execute(f"SELECT * FROM counting_guildsettings WHERE guild_id = {guild}")
        result = counting_cursor.fetchone()

        if result[2] != 0:
            counting_cursor.execute(f"UPDATE counting_guildsettings SET counting_channel_id = 0 WHERE guild_id = {guild}")
            counting_cursor.execute(f"UPDATE counting_guildsettings SET maxcount = 2147483647 WHERE guild_id = {guild}")
            counting_cursor.execute(f"UPDATE counting_guildsettings SET restart_on_error = 0 WHERE guild_id = {guild}")
            counting_cursor.execute(f"DELETE FROM counting_data WHERE guild_id = {guild}")
            db_counting.commit()

            embed = discord.Embed(
                description=f"**Reset Complete!** Do `!setup` to activate the bot again!",
                color=settings.embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=settings.footer)
            await ctx.send(embed=embed)
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

    @setup.error
    async def setup_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have enough permissions. "
                           "You need to have the **MANAGE_SERVER** permission to use this command.")
        error = getattr(error, "original", error)
        if isinstance(error, discord.Forbidden):
            await ctx.send("The bot has not enough permissions. "
                           "Try giving the bot Administrator Permissions to do the setup command. "
                           "Then you can remove those permissions.")

    @reset.error
    async def reset_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have enough permissions. "
                           "You need to have the **ADMINISTRATOR** permission to use this command.")

    @autosetup.error
    async def autosetup_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have enough permissions. "
                           "You need to have the **MANAGE_SERVER** permission to use this command.")
        error = getattr(error, "original", error)
        if isinstance(error, discord.Forbidden):
            await ctx.send("The bot has not enough permissions. "
                           "Try giving the bot Administrator Permissions to do the setup command. "
                           "Then you can remove those permissions.")


def setup(client):
    client.add_cog(ManualSetup(client))
