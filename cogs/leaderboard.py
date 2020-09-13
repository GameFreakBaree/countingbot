import discord
from discord.ext import commands
import datetime
from data import settings
import mysql.connector


class Leaderboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["lb", "scoreboard", "top"])
    async def leaderboard(self, ctx, page=1):
        guild = ctx.guild.id
        db_counting = mysql.connector.connect(host=settings.host, user=settings.user, passwd=settings.passwd,
                                              database=settings.database)
        counting_cursor = db_counting.cursor()

        pre_offset = page - 1
        offset = pre_offset * 10

        after_str = ""
        first_followup = offset

        counting_cursor.execute(
            f"SELECT * FROM counting_userdata WHERE guild_id = {guild} ORDER BY count DESC LIMIT 10 OFFSET {offset}")
        result = counting_cursor.fetchall()
        for row in result:
            first_followup = first_followup + 1

            try:
                top_name = self.client.get_user(row[2])
                top_names = top_name.mention
            except AttributeError:
                top_names = row[2]

            total_user_counts = f"score: {row[3]}"

            pre_str = f"**{first_followup}.** {top_names} • **{total_user_counts}**\n"
            after_str = after_str + pre_str

        if after_str == "":
            after_str = "No Data Found!"

        all_counts = 0
        counting_cursor.execute(f"SELECT count FROM counting_userdata WHERE guild_id = {guild}")
        counts = counting_cursor.fetchall()
        for row in counts:
            all_counts = all_counts + row[0]

        embed = discord.Embed(
            title=f"Leaderboard [Page {page}]",
            description=f"__Total Count:__ {all_counts}\n\n{after_str}",
            color=settings.embedcolor,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=settings.footer)
        await ctx.send(embed=embed)
        db_counting.close()


def setup(client):
    client.add_cog(Leaderboard(client))
