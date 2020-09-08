from discord.ext import commands

import os
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

import methods
from discord_utils.embeds import simple_embed

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='balance',
        description='get the balance in an account',
        aliases=['b', "bal", "my-bal"]
    )
    async def balance(self, ctx, wallet=None):
        if wallet is None:
            wallet=ctx.author.mention
        get_wallet_result = methods.get_wallet(ctx.guild, wallet)        
        if(get_wallet_result[0]):
            found_wallet = methods.find_create(get_wallet_result[1].id, ctx.guild)
            print(found_wallet,"found_wallet")
            if "permissions" in found_wallet:
                if "view" in found_wallet["permissions"]:
                    print(1)
                    if ctx.author.id in found_wallet["permissions"]["view"]["false"]:
                        print(2)
                        return await ctx.send(embed=simple_embed((False, "you do not have permission to see this wallet")))
            res = ""
            for key,value in found_wallet.items():
                if("balance" in key):
                    res = res+ f'{key}: {value}\n'
            return await ctx.send(embed=simple_embed(True,f'the balance is:\n {res}'))
        else:
            return await ctx.send(embed=simple_embed( False, "doesn't exist"))

def setup(bot):
    bot.add_cog(Balance(bot))