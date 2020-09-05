from discord.ext import commands
import mysql.connector
from data import settings

db_counting = mysql.connector.connect(
    host=settings.host,
    user=settings.user,
    passwd=settings.passwd,
    database=settings.database
)


class OnReady(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db_counting.commit()
        counting_cursor = db_counting.cursor()

        instertdata = "INSERT INTO counting_data (guild_id, number, last_user_id) VALUES (%s, %s, %s)"
        record2 = (f"{guild.id}", 0, 0)
        counting_cursor.execute(instertdata, record2)
        db_counting.commit()

        instertguildsettings = "INSERT INTO counting_guildsettings (guild_id, counting_channel_id, maxcount, restart_on_error) VALUES (%s, %s, %s, %s)"
        record3 = (f"{guild.id}", 0, 2147483647, 0)
        counting_cursor.execute(instertguildsettings, record3)
        db_counting.commit()


def setup(client):
    client.add_cog(OnReady(client))
