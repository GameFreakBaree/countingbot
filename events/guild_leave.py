from discord.ext import commands
import mysql.connector
from data import settings


class EventsGuildLeave(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        db_counting = mysql.connector.connect(host=settings.host, database=settings.database, user=settings.user,
                                              passwd=settings.passwd)
        counting_cursor = db_counting.cursor()
        counting_cursor.execute(f"DELETE FROM counting_userdata WHERE guild_id = {guild.id}")
        counting_cursor.execute(f"DELETE FROM counting_data WHERE guild_id = {guild.id}")
        counting_cursor.execute(f"DELETE FROM counting_guildsettings WHERE guild_id = {guild.id}")
        db_counting.commit()


def setup(client):
    client.add_cog(EventsGuildLeave(client))
