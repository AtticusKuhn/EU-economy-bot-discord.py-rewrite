from discord.ext import commands
import re
import time

import os
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

import methods
from discord_utils.embeds import simple_embed
from config import config
from commands.send import send
from commands.alter_money import Alter_Money

class Smart_contract(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='add-smart-contract',
        description='add a new smart contract',
        aliases=['sc']
    )
    async def insert_trade(self, ctx,trigger, *,contract):
        print("contract", contract)
        return
        guild=ctx.guild
        person=ctx.author
        if(trigger not in config["triggers"]):
            return (False, f'invalid trigger types. The supported types are {config["triggers"]}')
        for i in config["illegal_code"]:
            if(i in contract):
                return (False, "contains malicious code")
        if "set_money" in contract and not person.guild_permissions.administrator:
            return (False, "only admins can use set_money")
        guild_collection =db[str(guild.id)]
        contracts = guild_collection.find({
            "type":"contract",
            "author":person.id
        })
        if(len(list(contracts)) > config["max_contracts"]):
            return (False, "you have too many contracts")
        guild_collection.insert_one({
            "type"   :"contract",
            "author":person.id,
            "trigger": trigger,
            "code": contract,
            "guild_id":guild.id
        })
        return (True, "successful")


def setup(bot):
    bot.add_cog(Smart_contract(bot))


def execute_contracts(guild,array_of_contracts ,context, context_name):
    guild_collection =db[str(guild.id)]
    result = []
    for contract in array_of_contracts:
        safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'de grees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', "message", "context","locals"] 
        safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ]) 
        safe_dict["send"] = send
        safe_dict["whois"] = methods.whois
        safe_dict["set_money"] = Alter_Money.set_money
        safe_dict["guild"]=guild
        safe_dict['time'] = time
        safe_dict[context_name]=context
        try:
            exec(contract["code"],{"__builtins__":None},safe_dict)
            reply = str(safe_dict["output"])
        except Exception as e:
            reply = f'error:{e}'
        if(len(reply) > config["max_length"]):
            guild_collection.delete_one( { "_id" : contract["_id"]} )
            result.append((False, "message too long", contract["author"]))
        elif("error" in reply or "annul" in reply):
            guild_collection.delete_one( { "_id" : contract["_id"]} )
            result.append((False, reply, contract["author"]))
        else:
            result.append((True, reply, contract["author"]))
    return result
