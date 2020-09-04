import discord
from discord.ext import commands
import mysql.connector
from data import settings

db_counting = mysql.connector.connect(
    host=settings.host,
    database=settings.database,
    user=settings.user,
    passwd=settings.passwd
)


class Counting(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is False:
            db_counting.commit()
            counting_cursor = db_counting.cursor()

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

                    counting_cursor.execute(f"SELECT number FROM counting_data WHERE guild_id = {guild}")
                    number_tuple = counting_cursor.fetchone()
                    number = int(number_tuple[0])

                    try:
                        if resetonfail == 0:
                            message_inhoud = int(message.content)
                            if message_inhoud == number + 1:
                                counting_cursor.execute(
                                    f"SELECT maxcount FROM counting_guildsettings WHERE guild_id = {guild}")
                                maxcount_tuple = counting_cursor.fetchone()
                                maxcount = int(maxcount_tuple[0])

                                # Emote React START #
                                counting_cursor.execute(
                                    f"SELECT emote_react FROM counting_guildsettings WHERE guild_id = {guild}")
                                emotereact_tuple = counting_cursor.fetchone()
                                emotereact = int(emotereact_tuple[0])

                                if emotereact == 0:
                                    await message.add_reaction(emoji=settings.succes_emote)
                                # Emote React STOP #

                                counting_cursor.execute(
                                    f"SELECT user_id FROM counting_userdata WHERE user_id = {message.author.id} AND guild_id = {guild}")
                                user_id = counting_cursor.fetchone()

                                if user_id is None:
                                    instert_new_user_id = "INSERT INTO counting_userdata (guild_id, user_id, count) VALUES (%s, %s, %s)"
                                    countingbot_record = (guild, message.author.id, 1)
                                    counting_cursor.execute(instert_new_user_id, countingbot_record)
                                    db_counting.commit()
                                else:
                                    counting_cursor.execute(
                                        f"UPDATE counting_userdata SET count = count + 1 WHERE guild_id = {guild}")
                                    db_counting.commit()

                                if number + 1 == maxcount:
                                    counting_cursor.execute(
                                        f"UPDATE counting_data SET last_user_id = {message.author.id} WHERE guild_id = {guild}")
                                    counting_cursor.execute(
                                        f"UPDATE counting_data SET number = 0 WHERE guild_id = {guild}")
                                    db_counting.commit()

                                    counting_channel = self.client.get_channel(counting_channel_id[0])

                                    embed = discord.Embed(
                                        title="Count Reset!",
                                        description=f"Maximum count archieved ({maxcount})! Count reset to 0.",
                                        color=settings.embedcolor
                                    )
                                    embed.set_author(name=self.client.user.display_name,
                                                     icon_url=self.client.user.avatar_url)
                                    embed.set_footer(text=settings.footer)
                                    await counting_channel.send(embed=embed)
                                else:
                                    counting_cursor.execute(
                                        f"UPDATE counting_data SET last_user_id = {message.author.id} WHERE guild_id = {guild}")
                                    counting_cursor.execute(
                                        f"UPDATE counting_data SET number = {number + 1} WHERE guild_id = {guild}")
                                    db_counting.commit()
                        else:
                            message_inhoud = int(message.content)
                            if message_inhoud == number + 1:
                                counting_cursor.execute(
                                    f"SELECT maxcount FROM counting_guildsettings WHERE guild_id = {guild}")
                                maxcount_tuple = counting_cursor.fetchone()
                                maxcount = int(maxcount_tuple[0])

                                # Emote React START #
                                counting_cursor.execute(
                                    f"SELECT emote_react FROM counting_guildsettings WHERE guild_id = {guild}")
                                emotereact_tuple = counting_cursor.fetchone()
                                emotereact = int(emotereact_tuple[0])

                                if emotereact == 0:
                                    await message.add_reaction(emoji=settings.succes_emote)
                                # Emote React STOP #

                                counting_cursor.execute(
                                    f"SELECT user_id FROM counting_userdata WHERE user_id = {message.author.id} AND guild_id = {guild}")
                                user_id = counting_cursor.fetchone()

                                if user_id is None:
                                    instert_new_user_id = "INSERT INTO counting_userdata (guild_id, user_id, count) VALUES (%s, %s, %s)"
                                    countingbot_record = (guild, message.author.id, 1)
                                    counting_cursor.execute(instert_new_user_id, countingbot_record)
                                    db_counting.commit()
                                else:
                                    counting_cursor.execute(
                                        f"UPDATE counting_userdata SET count = count + 1 WHERE guild_id = {guild}")
                                    db_counting.commit()

                                if number + 1 == maxcount:
                                    counting_cursor.execute(
                                        f"UPDATE counting_data SET last_user_id = {message.author.id} WHERE guild_id = {guild}")
                                    counting_cursor.execute(
                                        f"UPDATE counting_data SET number = 0 WHERE guild_id = {guild}")
                                    db_counting.commit()

                                    counting_channel = self.client.get_channel(counting_channel_id[0])

                                    embed = discord.Embed(
                                        title="Count Reset!",
                                        description=f"Maximum count archieved ({maxcount})! Count reset to 0.",
                                        color=settings.embedcolor
                                    )
                                    embed.set_author(name=self.client.user.display_name,
                                                     icon_url=self.client.user.avatar_url)
                                    embed.set_footer(text=settings.footer)
                                    await counting_channel.send(embed=embed)
                                else:
                                    counting_cursor.execute(
                                        f"UPDATE counting_data SET last_user_id = {message.author.id} WHERE guild_id = {guild}")
                                    counting_cursor.execute(
                                        f"UPDATE counting_data SET number = {number + 1} WHERE guild_id = {guild}")
                                    db_counting.commit()
                            else:
                                counting_cursor.execute(
                                    f"UPDATE counting_data SET last_user_id = {message.author.id} WHERE guild_id = {guild}")
                                counting_cursor.execute(f"UPDATE counting_data SET number = 0 WHERE guild_id = {guild}")
                                db_counting.commit()

                                counting_channel = self.client.get_channel(counting_channel_id[0])

                                # Emote React START #
                                counting_cursor.execute(
                                    f"SELECT emote_react FROM counting_guildsettings WHERE guild_id = {guild}")
                                emotereact_tuple = counting_cursor.fetchone()
                                emotereact = int(emotereact_tuple[0])

                                if emotereact == 0:
                                    await message.add_reaction(emoji=settings.error_emote)
                                # Emote React STOP #

                                embed = discord.Embed(
                                    title="Count Reset!",
                                    description=f"Wrong number! The count has now been reset to 0.",
                                    color=settings.embedcolor
                                )
                                embed.set_author(name=self.client.user.display_name,
                                                 icon_url=self.client.user.avatar_url)
                                embed.set_footer(text=settings.footer)
                                await counting_channel.send(embed=embed)
                    except ValueError:
                        if resetonfail == 0:
                            await message.channel.purge(limit=1)
                        else:
                            counting_cursor.execute(
                                f"UPDATE counting_data SET last_user_id = {message.author.id} WHERE guild_id = {guild}")
                            counting_cursor.execute(f"UPDATE counting_data SET number = 0 WHERE guild_id = {guild}")
                            db_counting.commit()

                            counting_channel = self.client.get_channel(counting_channel_id[0])

                            counting_cursor.execute(
                                f"SELECT emote_react FROM counting_guildsettings WHERE guild_id = {guild}")
                            emotereact_tuple = counting_cursor.fetchone()
                            emotereact = int(emotereact_tuple[0])

                            if emotereact == 0:
                                await message.add_reaction(emoji=settings.error_emote)

                            embed = discord.Embed(
                                title="Count Reset!",
                                description=f"Wrong number! The count has now been reset to 0.",
                                color=settings.embedcolor
                            )
                            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                            embed.set_footer(text=settings.footer)
                            await counting_channel.send(embed=embed)


def setup(client):
    client.add_cog(Counting(client))
