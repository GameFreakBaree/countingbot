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


class OnReady(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db_counting.commit()
        counting_cursor = db_counting.cursor()

        instertguilddata = "INSERT INTO counting_guilddata (guild_id, totalcount) VALUES (%s, %s)"
        record1 = (f"{guild.id}", 0)
        counting_cursor.execute(instertguilddata, record1)
        db_counting.commit()

        instertdata = "INSERT INTO counting_data (guild_id, number, last_user_id) VALUES (%s, %s, %s)"
        record2 = (f"{guild.id}", 0, 0)
        counting_cursor.execute(instertdata, record2)
        db_counting.commit()

        instertguildsettings = "INSERT INTO counting_guildsettings (guild_id, prefix, counting_channel_id, maxcount, restart_on_error) VALUES (%s, %s, %s, %s, %s)"
        record3 = (f"{guild.id}", "c!", 0, 2147483647, 0)
        counting_cursor.execute(instertguildsettings, record3)
        db_counting.commit()


def setup(client):
    client.add_cog(OnReady(client))
