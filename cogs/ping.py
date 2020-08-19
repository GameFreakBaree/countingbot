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


class PingCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        ping = round(self.client.latency * 1000)

        if ping > 1000:
            emote = "<:red_status:742804156888121424>"
        elif 1000 >= ping >= 250:
            emote = "<:orange_status:742804156716417075>"
        else:
            emote = "<:green_status:742804157043441694>"

        embed = discord.Embed(
            description=f"{emote} **Ping:** {ping}ms",
            color=embed_color
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=embed_footer[0])
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(PingCmd(client))
