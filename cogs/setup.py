import discord
from discord.ext import commands
import datetime
import mysql.connector
from discord.ext.commands import MissingPermissions
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


class ManualSetup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx):
        guild = ctx.guild.id
        db_counting.commit()
        counting_cursor = db_counting.cursor()

        counting_cursor.execute("SELECT footer FROM counting_settings")
        embed_footer = counting_cursor.fetchone()

        counting_cursor.execute("SELECT embed_color FROM counting_settings")
        embed_color_tuple = counting_cursor.fetchone()
        embed_color = int(embed_color_tuple[0], 16)

        counting_cursor.execute(f"SELECT * FROM counting_guildsettings WHERE guild_id = {guild}")
        result = counting_cursor.fetchall()
        result_tuple = result[0]
        if result_tuple[2] == 0:
            await ctx.channel.set_permissions(self.client.user, send_messages=True, read_messages=True,
                                              add_reactions=True, embed_links=True, manage_messages=True,
                                              read_message_history=True, external_emojis=True,
                                              manage_permissions=True)

            channel_id_updatesql = f"UPDATE counting_guildsettings SET counting_channel_id = {ctx.channel.id} WHERE guild_id = {guild}"
            counting_cursor.execute(channel_id_updatesql)
            db_counting.commit()

            embed = discord.Embed(
                description=f"**Setup Complete!** You can now use the counting features!\n"
                            f"\nIf the bot does not add emotes or delete false messages, please make sure that"
                            f"the bot has the permissions in the channel. Otherwise, give Administrator to the bot",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=embed_footer[0])
            await ctx.author.send(embed=embed)
        else:
            embed = discord.Embed(
                description=f"**Setup Failed!** You already did the setup command!",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=embed_footer[0])
            await ctx.author.send(embed=embed)

    @commands.command()
    async def autosetup(self, ctx):
        guild = ctx.guild.id
        db_counting.commit()
        counting_cursor = db_counting.cursor()

        counting_cursor.execute("SELECT footer FROM counting_settings")
        embed_footer = counting_cursor.fetchone()

        counting_cursor.execute("SELECT embed_color FROM counting_settings")
        embed_color_tuple = counting_cursor.fetchone()
        embed_color = int(embed_color_tuple[0], 16)

        counting_cursor.execute(f"SELECT * FROM counting_guildsettings WHERE guild_id = {guild}")
        result = counting_cursor.fetchall()
        result_tuple = result[0]
        if result_tuple[2] == 0:
            counting_channel = await ctx.guild.create_text_channel('counting')
            await counting_channel.set_permissions(self.client.user, send_messages=True, read_messages=True,
                                                   add_reactions=True, embed_links=True, manage_messages=True,
                                                   read_message_history=True, external_emojis=True,
                                                   manage_permissions=True)

            channel_id_updatesql = f"UPDATE counting_guildsettings SET counting_channel_id = {counting_channel.id} WHERE guild_id = {guild}"
            counting_cursor.execute(channel_id_updatesql)
            db_counting.commit()

            embed = discord.Embed(
                description=f"**Auto Setup Complete!** You can now use the counting features!",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description=f"**Auto Setup Failed!** You already did the setup command!",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx):
        guild = ctx.guild.id
        db_counting.commit()
        counting_cursor = db_counting.cursor()

        counting_cursor.execute("SELECT footer FROM counting_settings")
        embed_footer = counting_cursor.fetchone()

        counting_cursor.execute("SELECT embed_color FROM counting_settings")
        embed_color_tuple = counting_cursor.fetchone()
        embed_color = int(embed_color_tuple[0], 16)

        counting_cursor.execute(f"SELECT * FROM counting_guildsettings WHERE guild_id = {guild}")
        result = counting_cursor.fetchone()

        if result[2] != 0:
            embed = discord.Embed(
                description=f"**Reset Complete!** Do `!setup` to activate the bot again!",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=embed)

            channel_id_updatesql1 = f"UPDATE counting_guildsettings SET counting_channel_id = 0 WHERE guild_id = {guild}"
            counting_cursor.execute(channel_id_updatesql1)
            db_counting.commit()

            channel_id_updatesql2 = f"UPDATE counting_guildsettings SET prefix = c! WHERE guild_id = {guild}"
            counting_cursor.execute(channel_id_updatesql2)
            db_counting.commit()

            channel_id_updatesql3 = f"UPDATE counting_guildsettings SET maxcount = 2147483647 WHERE guild_id = {guild}"
            counting_cursor.execute(channel_id_updatesql3)
            db_counting.commit()

            channel_id_updatesql4 = f"UPDATE counting_guildsettings SET restart_on_error = 0 WHERE guild_id = {guild}"
            counting_cursor.execute(channel_id_updatesql4)
            db_counting.commit()

            # my_sql1 = f"DELETE FROM counting_guilddata WHERE guild_id = {guild}"
            # counting_cursor.execute(my_sql1)
            # db_counting.commit()
            #
            # my_sql2 = f"DELETE FROM counting_userdata WHERE guild_id = {guild}"
            # counting_cursor.execute(my_sql2)
            # db_counting.commit()

            my_sql3 = f"DELETE FROM counting_data WHERE guild_id = {guild}"
            counting_cursor.execute(my_sql3)
            db_counting.commit()
        else:
            embed = discord.Embed(
                description=f"**Reset Failed!** No setup was done!",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=embed)

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
