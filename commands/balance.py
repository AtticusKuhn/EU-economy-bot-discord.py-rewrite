from discord.ext import commands

import os
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

#import methods
from discord_utils.embeds import simple_embed
from database_utils.wallet_converter import WalletConverter

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='balance',
        description='get the balance in an account',
        aliases=['b', "bal", "my-bal"]
    )
    async def balance(self, ctx, wallet:WalletConverter):
        if "permissions" in wallet:
            if "view" in wallet["permissions"]:
                print(1)
                if ctx.author.id in wallet["permissions"]["view"]["false"]:
                    print(2)
                    return await ctx.send(embed=simple_embed((False, "you do not have permission to see this wallet")))
        res = ""
        for key,value in wallet.items():
            if("balance" in key):
                res = res+ f'{key}: {value}\n'
        return await ctx.send(embed=simple_embed(True,f'the balance is:\n {res}'))

def setup(bot):
    bot.add_cog(Balance(bot))