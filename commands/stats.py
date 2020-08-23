from discord.ext import commands
import discord
import matplotlib.pyplot as plt 

import os
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

import methods
from discord_utils.embeds import simple_embed

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='graph',
        description='graph the money over time of an account',
        aliases=['gr']
    )
    async def graph(self, ctx, wallet):
        result = methods.get_wallet(ctx.guild, wallet)
        if(result[0]):
            print(result)
            found_wallet = methods.find_create(result[1].id,ctx.guild)
            if "record" in found_wallet:
                fig = plt.figure(figsize=(10,5))
                X1 = list(found_wallet["record"].keys())
                Y1 = list(found_wallet["record"].values())

                plt.plot(X1, Y1, label = "plot 1")
                fig.savefig('fig.jpg', bbox_inches='tight', dpi=150)
                return await ctx.send(file=discord.File('fig.jpg'))
                os.remove("fig.jpg")
            else:
                return await ctx.send(embed=simple_embed(False,"can't find any stats"))
        else:
            await ctx.send(embed=simple_embed(False,"error"))
    
def setup(bot):
    bot.add_cog(Stats(bot))