from discord.ext import commands
from data import settings
import mysql.connector


class SetTopic(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def settopic(self, ctx, *, topic=None):
        guild = ctx.guild.id
        db_counting = mysql.connector.connect(host=settings.host, user=settings.user, passwd=settings.passwd,
                                              database=settings.database)
        counting_cursor = db_counting.cursor()

        counting_cursor.execute(f"SELECT counting_channel_id FROM counting_guildsettings WHERE guild_id = {guild}")
        counting_channel_id = counting_cursor.fetchone()
        counting_channel = self.client.get_channel(counting_channel_id[0])

        if topic is not None:
            await counting_channel.edit(topic=topic)
        else:
            await ctx.send("Please give a Topic to change.")

        db_counting.close()

    @settopic.error
    async def settopic_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            return


def setup(client):
    client.add_cog(SetTopic(client))
