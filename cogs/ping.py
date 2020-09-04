import discord
from discord.ext import commands
from data import settings


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
            color=settings.embedcolor
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=settings.footer)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(PingCmd(client))
