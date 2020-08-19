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


class Counting(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        db_counting.commit()
        counting_cursor = db_counting.cursor()

        if message.author.bot is False:
            guild = message.guild.id
            counting_cursor.execute(f"SELECT counting_channel_id FROM counting_guildsettings WHERE guild_id = {guild}")
            counting_channel_id = counting_cursor.fetchone()
            if message.channel.id == counting_channel_id[0]:
                counting_cursor.execute(f"SELECT last_user_id FROM counting_data WHERE guild_id = {guild}")
                vorige_id_tuple = counting_cursor.fetchone()
                vorige_id = int(vorige_id_tuple[0])

                if message.author.id == vorige_id:
                    await message.channel.purge(limit=1)
                else:
                    counting_cursor.execute(
                        f"SELECT restart_on_error FROM counting_guildsettings WHERE guild_id = {guild}")
                    resetonfail_tuple = counting_cursor.fetchone()
                    resetonfail = int(resetonfail_tuple[0])

                    counting_cursor.execute("SELECT footer FROM counting_settings")
                    embed_footer = counting_cursor.fetchone()

                    counting_cursor.execute("SELECT embed_color FROM counting_settings")
                    embed_color_tuple = counting_cursor.fetchone()
                    embed_color = int(embed_color_tuple[0], 16)

                    counting_cursor.execute(f"SELECT error_emote FROM counting_settings")
                    error_emote_tuple = counting_cursor.fetchone()
                    error_emote = str(error_emote_tuple[0])

                    try:
                        counting_cursor.execute(f"SELECT success_emote FROM counting_settings")
                        check_emote_tuple = counting_cursor.fetchone()
                        check_emote = str(check_emote_tuple[0])

                        counting_cursor.execute(f"SELECT number FROM counting_data WHERE guild_id = {guild}")
                        number_tuple = counting_cursor.fetchone()
                        number = int(number_tuple[0])

                        if resetonfail == 0:
                            message_inhoud = int(message.content)
                            if message_inhoud == number + 1:
                                counting_cursor.execute(
                                    f"SELECT maxcount FROM counting_guildsettings WHERE guild_id = {guild}")
                                maxcount_tuple = counting_cursor.fetchone()
                                maxcount = int(maxcount_tuple[0])

                                if number + 1 == maxcount:
                                    update_sql_member_maxcount = f"UPDATE counting_data SET last_user_id = {message.author.id} WHERE guild_id = {guild}"
                                    counting_cursor.execute(update_sql_member_maxcount)
                                    db_counting.commit()

                                    update_sql_nr_maxcount = f"UPDATE counting_data SET number = 0 WHERE guild_id = {guild}"
                                    counting_cursor.execute(update_sql_nr_maxcount)
                                    db_counting.commit()

                                    counting_channel = self.client.get_channel(counting_channel_id[0])
                                    await message.add_reaction(emoji=check_emote)

                                    embed = discord.Embed(
                                        title="Count Reset!",
                                        description=f"Maximum count archieved ({maxcount})! Count reset to 0.",
                                        color=embed_color
                                    )
                                    embed.set_author(name=self.client.user.display_name,
                                                     icon_url=self.client.user.avatar_url)
                                    embed.set_footer(text=embed_footer[0])
                                    await counting_channel.send(embed=embed)
                                else:
                                    await message.add_reaction(emoji=check_emote)

                                    update_sql_member = f"UPDATE counting_data SET last_user_id = {message.author.id} WHERE guild_id = {guild}"
                                    counting_cursor.execute(update_sql_member)
                                    db_counting.commit()

                                    update_sql_nr = f"UPDATE counting_data SET number = {number + 1} WHERE guild_id = {guild}"
                                    counting_cursor.execute(update_sql_nr)
                                    db_counting.commit()
                            else:
                                await message.channel.purge(limit=1)
                                print(f"Error: Message_inhoud != number+1 in guild: {guild}")
                        else:
                            message_inhoud = int(message.content)
                            if message_inhoud == number + 1:
                                counting_cursor.execute(
                                    f"SELECT maxcount FROM counting_guildsettings WHERE guild_id = {guild}")
                                maxcount_tuple = counting_cursor.fetchone()
                                maxcount = int(maxcount_tuple[0])

                                if number + 1 == maxcount:
                                    update_sql_member_maxcount = f"UPDATE counting_data SET last_user_id = {message.author.id} WHERE guild_id = {guild}"
                                    counting_cursor.execute(update_sql_member_maxcount)
                                    db_counting.commit()

                                    update_sql_nr_maxcount = f"UPDATE counting_data SET number = 0 WHERE guild_id = {guild}"
                                    counting_cursor.execute(update_sql_nr_maxcount)
                                    db_counting.commit()

                                    counting_cursor.execute("SELECT footer FROM counting_settings")
                                    embed_footer = counting_cursor.fetchone()

                                    counting_cursor.execute("SELECT embed_color FROM counting_settings")
                                    embed_color_tuple = counting_cursor.fetchone()
                                    embed_color = int(embed_color_tuple[0], 16)

                                    counting_channel = self.client.get_channel(counting_channel_id[0])
                                    await message.add_reaction(emoji=check_emote)

                                    embed = discord.Embed(
                                        title="Count Reset!",
                                        description=f"Maximum count archieved ({maxcount})! Count reset to 0.",
                                        color=embed_color
                                    )
                                    embed.set_author(name=self.client.user.display_name,
                                                     icon_url=self.client.user.avatar_url)
                                    embed.set_footer(text=embed_footer[0])
                                    await counting_channel.send(embed=embed)
                                else:
                                    await message.add_reaction(emoji=check_emote)

                                    update_sql_member = f"UPDATE counting_data SET last_user_id = {message.author.id} WHERE guild_id = {guild}"
                                    counting_cursor.execute(update_sql_member)
                                    db_counting.commit()

                                    update_sql_nr = f"UPDATE counting_data SET number = {number + 1} WHERE guild_id = {guild}"
                                    counting_cursor.execute(update_sql_nr)
                                    db_counting.commit()
                            else:
                                update_sql_member_maxcount = f"UPDATE counting_data SET last_user_id = {message.author.id} WHERE guild_id = {guild}"
                                counting_cursor.execute(update_sql_member_maxcount)
                                db_counting.commit()

                                update_sql_nr_maxcount = f"UPDATE counting_data SET number = 0 WHERE guild_id = {guild}"
                                counting_cursor.execute(update_sql_nr_maxcount)
                                db_counting.commit()

                                counting_channel = self.client.get_channel(counting_channel_id[0])
                                await message.add_reaction(emoji=error_emote)

                                embed = discord.Embed(
                                    title="Count Reset!",
                                    description=f"Wrong number! The count has now been reset to 0.",
                                    color=embed_color
                                )
                                embed.set_author(name=self.client.user.display_name,
                                                 icon_url=self.client.user.avatar_url)
                                embed.set_footer(text=embed_footer[0])
                                await counting_channel.send(embed=embed)
                    except ValueError:
                        if resetonfail == 0:
                            await message.channel.purge(limit=1)
                        else:
                            update_sql_member_maxcount = f"UPDATE counting_data SET last_user_id = {message.author.id} WHERE guild_id = {guild}"
                            counting_cursor.execute(update_sql_member_maxcount)
                            db_counting.commit()

                            update_sql_nr_maxcount = f"UPDATE counting_data SET number = 0 WHERE guild_id = {guild}"
                            counting_cursor.execute(update_sql_nr_maxcount)
                            db_counting.commit()

                            counting_channel = self.client.get_channel(counting_channel_id[0])
                            await message.add_reaction(emoji=error_emote)

                            embed = discord.Embed(
                                title="Count Reset!",
                                description=f"Wrong number! The count has now been reset to 0.",
                                color=embed_color
                            )
                            embed.set_author(name=self.client.user.display_name,
                                             icon_url=self.client.user.avatar_url)
                            embed.set_footer(text=embed_footer[0])
                            await counting_channel.send(embed=embed)


def setup(client):
    client.add_cog(Counting(client))
