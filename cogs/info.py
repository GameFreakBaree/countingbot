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


class InfoCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx):
        db_counting = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)

        counting_cursor = db_counting.cursor()
        counting_cursor.execute("SELECT footer FROM counting_settings")
        embed_footer = counting_cursor.fetchone()

        counting_cursor.execute("SELECT embed_color FROM counting_settings")
        embed_color_tuple = counting_cursor.fetchone()
        embed_color = int(embed_color_tuple[0], 16)

        embed = discord.Embed(
            description=f"__Created by:__ GameFreakBaree#9999\n__Shard:__ 1/1\n\n**Useful URLs**\n[Invite the Bot](https://discord.com/oauth2/authorize?client_id=742776969481158766&permissions=1074097233&redirect_uri=https%3A%2F%2Fdiscord.gg%2F5gvn5pn&scope=bot) - [Wiki](https://github.com/GameFreakBaree/countingbot/wiki) - [Support Server](https://discord.gg/5gvn5pn)",
            color=embed_color
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=embed_footer[0])
        await ctx.send(embed=embed)

        db_counting.close()


def setup(client):
    client.add_cog(InfoCmd(client))
