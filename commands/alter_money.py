from discord.ext import commands

import os
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

import methods
from discord_utils.embeds import simple_embed
from database_utils.wallet_converter import WalletConverter

class Alter_Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='print',
        description='add an amount of money to an account',
        aliases=['pt']
    )
    async def print_money(self, ctx, account_of_printing:WalletConverter, amount):
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
        can_print = False
        if person.guild_permissions.administrator:
            can_print=True
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
    @commands.has_permissions(administrator=True)   
    async def set_money(self, ctx, wallet:WalletConverter, amount):
        result = await set_money(ctx.guild, wallet, amount)
        return await ctx.send(embed=simple_embed(*result))
    @commands.command(
        name='set-money-each',
        description='set the amount of money of each person who satisfies a condition',
        aliases=['set-bal-ea', "set-balance-each","sbe"]
    )
    @commands.has_permissions(administrator=True)    
    async def set_balance_each(self, ctx, amount,*, condition): 
        print("amount is", amount)
        print("condition is", condition)
        return_statement = ""
        successful_transfer = True
        people = methods.whois(condition.split(" "), ctx.guild)
        for person in people:
            wc = WalletConverter()
            person = await wc.convert(ctx, f'<@{person}>')
            send_result = await set_money(ctx.guild, person,amount)
            if  send_result[0]:
                return_statement = return_statement + f'<@{person["id"]}> - success\n'
            else:
                return_statement = return_statement + f'<@{person["id"]}> - error: {send_result[1]}\n'
                successful_transfer = False
        if return_statement == "":
            return_statement = "(no people found)"
        return await ctx.channel.send(embed=simple_embed(successful_transfer,return_statement ))
def setup(bot):
    bot.add_cog(Alter_Money(bot))


async def set_money(guild, wallet, amount):
    if("-" in amount):
            amount_array = amount.split("-")
            amount = amount_array[0]
            currency = amount_array[1]
    if 'currency' in locals():
        if(not methods.valid_item(currency)):
            return  (False, "invaid item name")
    if(not amount.isdigit()):
        return  (False, "incorrect ammount")
    guild_collection =db[str(guild.id)]
    if 'currency' in locals():
        guild_collection.update_one(
            {"_id":  wallet["_id"] },
            { "$set":{f'balance-{currency}':int(amount)} }
        )
        return (True, f'balance was set to {amount}')
    guild_collection.update_one(
        {"_id":  wallet["_id"]  },
        { "$set":{"balance":int(amount)} }
    )
    return (True, f'balance was set to {amount}')
