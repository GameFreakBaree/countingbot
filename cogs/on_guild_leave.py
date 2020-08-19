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
    async def on_guild_remove(self, guild):
        db_counting.commit()
        counting_cursor = db_counting.cursor()

        dropguilddata = f"DELETE FROM counting_guilddata WHERE guild_id = {guild.id}"
        counting_cursor.execute(dropguilddata)
        db_counting.commit()

        dropdata = f"DELETE FROM counting_data WHERE guild_id = {guild.id}"
        counting_cursor.execute(dropdata)
        db_counting.commit()

        dropguildsettings = f"DELETE FROM counting_guildsettings WHERE guild_id = {guild.id}"
        counting_cursor.execute(dropguildsettings)
        db_counting.commit()


def setup(client):
    client.add_cog(OnReady(client))
