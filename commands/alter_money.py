from discord.ext import commands

import os
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

import methods
from discord_utils.embeds import simple_embed

class Alter_Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='print',
        description='add an amount of money to an account',
        aliases=['pt']
    )
    async def print_money(self, ctx, wallet, amount):
        person = ctx.author
        currency=""
        if "-" in amount:
            currency=f'-{amount.split("-")[1]}'
            amount =amount.split("-")[0]

            if not methods.valid_item(currency[1:]):
                return await ctx.send(embed=simple_embed(False, "invalid item name"))
        try:
            amount = int(amount)
        except:
            return await ctx.send(embed=simple_embed(False,"invalid amount" ))
        
        guild_collection =db[str(ctx.guild.id)]
        wallet_id = methods.get_wallet(ctx.guild, wallet)
        if not wallet_id[0]:
            return await ctx.send(embed=simple_embed(False,"invalid wallet name"))
        can_print = False
        if person.guild_permissions.administrator:
            can_print=True
        account_of_printing =methods.find_create(wallet_id[1].id,ctx.guild)
        if "permissions" in account_of_printing:
            if "print" in account_of_printing["permissions"]:
                if person.id in account_of_printing["permissions"]["print"]["true"]:
                    can_print = True
                for role in person.roles:
                    if role.id in account_of_printing["permissions"]["print"]["true"]:
                        can_print = True
            if currency != "":
                if f'print{currency}' in account_of_printing["permissions"]:
                    if person.id in account_of_printing["permissions"][f'print{currency}']["true"]:
                        can_print = True
                    for role in person.roles:
                        if role.id in account_of_printing["permissions"][f'print{currency}']["true"]:
                            can_print = True
        if "printer" in person.roles:
            can_print=True
        if not can_print:
            return await ctx.send(embed=simple_embed(False, "you do not have permission to print"))
        guild_collection.update_one(
            {"id":  account_of_printing["id"] },
            { "$inc":{f'balance{currency}':amount} }
        )
        return await ctx.send(embed=simple_embed(True, "transfer successful"))
    @commands.command(
        name='set-money',
        description='set the amount of money',
        aliases=['set-bal', "set-balance"]
    )
    async def set_money(self, ctx, wallet, amount):
        if("-" in amount):
            amount_array = amount.split("-")
            print(amount.split("-"))
            amount = amount_array[0]
            currency = amount_array[1]
        if 'currency' in locals():
            if(not methods.valid_item(currency)):
                return await ctx.send(embed=simple_embed(False, "invaid item name"))
        if(not amount.isdigit()):
            return (False, "incorrect ammount")
        guild_collection =db[str(ctx.guild.id)]
        to_wallet = methods.get_wallet(ctx.guild, wallet)
        if(not to_wallet[0]):
            return await ctx.send(embed=simple_embed(False,to_wallet))
        found_wallet = methods.find_create(to_wallet[1].id, ctx.guild)
        if 'currency' in locals():
            guild_collection.update_one(
                {"id":  to_wallet[1].id },
                { "$set":{f'balance-{currency}':int(amount)} }
            )
            return await ctx.send(embed=simple_embed(True, f'balance was set to {amount}'))
        guild_collection.update_one(
            {"id":  to_wallet[1].id },
            { "$set":{"balance":int(amount)} }
        )
        return await ctx.send(embed=simple_embed(True, f'balance was set to {amount}'))
def setup(bot):
    bot.add_cog(Alter_Money(bot))