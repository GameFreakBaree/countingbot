import discord
from discord.ext import commands
import datetime
from data import settings
import mysql.connector


class UserInfo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["user", "users"])
    async def userinfo(self, ctx, *, member: discord.Member = None):
        guild = ctx.guild.id
        db_counting = mysql.connector.connect(host=settings.host, user=settings.user, passwd=settings.passwd,
                                              database=settings.database)
        counting_cursor = db_counting.cursor()

        if member is None:
            member = ctx.author

        joined_correct = member.joined_at.strftime("%d/%m/%Y")

        counting_cursor.execute(f"SELECT * FROM counting_userdata WHERE user_id = {ctx.author.id} AND guild_id = {guild}")
        userdata = counting_cursor.fetchone()

        if userdata is not None:
            user_count_data = userdata[3]
        else:
            user_count_data = 0

        db_counting.close()

        info_embed = discord.Embed(
            title=f"{member.display_name}",
            timestamp=datetime.datetime.utcnow(),
            color=settings.embedcolor
        )
        info_embed.add_field(name="User Info",
                             value=f"ID: {member.id}\n"
                                   f"Username: {member.display_name}\nTAG: #{member.discriminator}",
                             inline=False)
        info_embed.add_field(name="Joined at", value=joined_correct, inline=True)
        info_embed.add_field(name="Count", value=f"{user_count_data}", inline=True)
        info_embed.add_field(name="Highest Rank", value=member.top_role, inline=True)
        info_embed.set_thumbnail(url=member.avatar_url)
        info_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        info_embed.set_footer(text=settings.footer)
        await ctx.send(embed=info_embed)


def setup(client):
    client.add_cog(UserInfo(client))
