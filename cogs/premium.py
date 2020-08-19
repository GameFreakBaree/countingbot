import discord
from discord.ext import commands
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


class PremiumCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def premium(self, ctx):
        if ctx.guild.id != 743513613943439422:
            embed = discord.Embed(
                description=f"Premium has not been activated on this server.\nPlease buy premium to support the Developer to make the project/bot and all future projects better.\n\n[Buy Premium](https://www.patreon.com/countingbot) - [Support Server](https://discord.gg/5gvn5pn)",
                color=embed_color
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(PremiumCmd(client))
