from discord.ext import commands
from data import settings
import os


class CoreUnload(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def unload(self, ctx, types=None, extension=None):
        if ctx.author.id == 643072638075273248:
            if types is not None and extension is not None:
                if types.lower() in settings.folder_list:
                    if extension == "*":
                        for filenames in os.listdir(f'./{types}'):
                            if filenames.endswith('.py'):
                                print(f"Unload {extension}, by {ctx.author}")
                                self.client.unload_extension(f'{types}.{filenames[:-3]}')
                        await ctx.send(f"Unloaded all extensions in {types}, succes!")
                    else:
                        self.client.unload_extension(f'{types}.{extension}')
                        print(f"Unload {extension}, by {ctx.author} in {types}")
                        await ctx.send(f"Unload {extension}, succes!")


def setup(client):
    client.add_cog(CoreUnload(client))
