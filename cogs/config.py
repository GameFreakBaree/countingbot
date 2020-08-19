import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
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


class ConfigCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def config(self, ctx, setting=None, value=None):
        guild = ctx.guild.id
        db_counting.commit()
        counting_cursor = db_counting.cursor()

        counting_cursor.execute("SELECT footer FROM counting_settings")
        embed_footer = counting_cursor.fetchone()

        counting_cursor.execute("SELECT embed_color FROM counting_settings")
        embed_color_tuple = counting_cursor.fetchone()
        embed_color = int(embed_color_tuple[0], 16)

        if setting is None:
            embed = discord.Embed(
                title="Config: Help",
                description="c!config maxcount <number>\nc!config resetonfail <enabled/disabled>",
                color=embed_color
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=embed)
        elif setting == "maxcount":
            try:
                maxcount_number = int(value)
                if 50 <= maxcount_number <= 2147483647:
                    setting_sql_maxcount = f"UPDATE counting_guildsettings SET maxcount = {maxcount_number} WHERE guild_id = {guild}"
                    counting_cursor.execute(setting_sql_maxcount)
                    db_counting.commit()

                    embed = discord.Embed(
                        title="Config: Maxcount",
                        description=f"The maximum count has been set to {maxcount_number}.",
                        color=embed_color
                    )
                    embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    embed.set_footer(text=embed_footer[0])
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("The number has to be between 50 and 2147483647")
            except ValueError:
                await ctx.send("Invalid Arguments. Try: `c!config maxcount <number>`")
        elif setting == "resetonfail":
            if value.lower() == "enabled" or value.lower() == "disabled":
                if value.lower() == "enabled":
                    restartonerror = 1
                elif value.lower() == "disabled":
                    restartonerror = 0
                else:
                    restartonerror = 0
                setting_sql_resetonfail = f"UPDATE counting_guildsettings SET restart_on_error = {restartonerror} WHERE guild_id = {guild}"
                counting_cursor.execute(setting_sql_resetonfail)
                db_counting.commit()

                embed = discord.Embed(
                    title="Config: Reset On Fail",
                    description=f"Reset on failure has now been {value.lower()}.",
                    color=embed_color
                )
                embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                embed.set_footer(text=embed_footer[0])
                await ctx.send(embed=embed)
            else:
                await ctx.send("Invalid Arguments. Try: `c!config resetonfail <enabled/disabled>`")

    @config.error
    async def config_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return


def setup(client):
    client.add_cog(ConfigCmd(client))
