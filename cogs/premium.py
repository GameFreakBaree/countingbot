import discord
from discord.ext import commands
from data import settings


class PremiumCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def premium(self, ctx):
        embed = discord.Embed(
            description=f"Premium has not been activated on this server."
                        f"\nPlease buy premium to support the Developer to make the project/bot and all future projects better."
                        f"\n\n[Buy Premium](https://www.patreon.com/countingbot) - [Support Server](https://discord.gg/5gvn5pn)",
            color=settings.embedcolor
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=settings.footer)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(PremiumCmd(client))
