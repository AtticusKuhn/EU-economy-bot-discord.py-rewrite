from discord.ext import commands
import re
import time
import asyncio
import discord

import os
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

import methods
from discord_utils.embeds import simple_embed
from config import config

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='insert-trade',
        description='put a new trade on the market',
        aliases=['i-t']
    )
    async def insert_trade(self, ctx, wallet,offer, cost, *options):
        person=ctx.author
        guild= ctx.guild
        message=ctx.message
        if wallet !="admins":
            found_wallet=methods.get_wallet(guild,wallet)
            if not found_wallet[0]:
                return  await ctx.send(embed=simple_embed(False, "bad wallet"))
            if not methods.can_access_wallet(guild, person.id, wallet):
                return  await ctx.send(embed=simple_embed(False,"bad wallet 2"))
        offer_currency=""
        offer_amount = offer
        if "-" in offer:
            offer_currency=f'-{offer.split("-")[1]}'
            offer_amount =offer.split("-")[0]
            if not methods.valid_item(offer_currency[1:]):
                return  await ctx.send(embed=simple_embed(False, "invalid item name"))
        cost_currency=""
        cost_amount = cost
        if "-" in cost:
            cost_currency=f'-{cost.split("-")[1]}'
            cost_amount =cost.split("-")[0]
            if not methods.valid_item(cost_currency[1:]):
                return  await ctx.send(embed=simple_embed(False, "invalid item name"))
        if re.match(r'<@&?\d{18}>', offer) is not None:
            offer_currency = offer
            offer_amount="1"
        print(offer_amount,cost_amount)
        if not offer_amount.isdigit() or not cost_amount.isdigit():
            return  await ctx.send(embed=simple_embed(False, "invalid amount"))
        offer_amount=int(offer_amount)
        cost_amount=int(cost_amount)
        for index, option in enumerate(options):
            if "use" in option:
                if not option.split("use")[0].isdigit():
                    return  await ctx.send(embed=simple_embed(False, "invalid uses"))
                uses = option.split("use")[0]
            if "time" in option:
                if not option.split("time")[0].isdigit():
                    return  await ctx.send(embed=simple_embed(False, "invalid time"))
                offer_time = int(option.split("time")[0]) +time.time()
            if option=="whois":
                people_restrictions = options[index:]
        guild_collection =db[str(guild.id)]
        offer_schema = {
            "type":"trade",
            "person":person.id,
            "message_id":message.id,
            "offer_currency":offer_currency,
            "offer_amount":int(offer_amount),
            "cost_currency":cost_currency,
            "cost_amount":int(cost_amount)
        }
        if "found_wallet" in locals():
            offer_schema["wallet"] = found_wallet[1].id
        if "uses" in locals():
            offer_schema["uses"]=int(uses)
        if "offer_time" in locals():
            offer_schema["offer_time"]=int(offer_time)
        if "people_restrictions" in locals():
            offer_schema["people_restrictions"] = people_restrictions
        guild_collection.insert_one(offer_schema)
        return  await ctx.send(embed=simple_embed(True, f'succesful. In order to accept this trade, type "$accept {message.id} (ping wallet)", or you may react to the original message with ✅, in which case the money will be deducted from your personal account.'))
    @commands.command(
        name='accept-trade',
        description='put a new trade on the market',
        aliases=['a-t']
    )
    async def fulfill_trade(self, ctx,wallet, message):
        guild = ctx.guild
        person = ctx.author
        found_wallet = methods.get_wallet(guild, wallet)
        if not found_wallet[0]:
            return  await ctx.send(embed=simple_embed(False,"cant find wallet"))
        if not methods.can_access_wallet(guild, person.id, wallet):
            return  await ctx.send(embed=simple_embed(False, "cannot access wallet"))
        try:
            message=int(message)
        except:
            return  await ctx.send(embed=simple_embed(False,"invalid number"))
        guild_collection =db[str(guild.id)]
        found_offer=guild_collection.find_one({
            "type":"trade",
            "message_id"  :message
        })
        if found_offer is None:
            return  await ctx.send(embed=simple_embed(False, "can't find offer"))
        if "uses" in found_offer:
            if found_offer["uses"] <=0:
                guild_collection.delete_one({"message_id":found_offer["message_id"]})
                return  await ctx.send(embed=simple_embed(False,"offer has been used up"))
        if "offer_time" in found_offer:
            if time.time() > found_offer["offer_time"]:
                guild_collection.delete_one({"message_id":found_offer["message_id"]})
                return  await ctx.send(embed=simple_embed(False,"offer has run out of time"))
        if "people_restrictions" in found_offer:
            if person.id not in methods.whois(found_offer["people_restrictions"],guild):
                return  await ctx.send(embed=simple_embed(False, "you cannot accept this offer because a restriction has bee"))
        receiver = methods.find_create(found_wallet[1].id,ctx.guild)
        if f'balance{found_offer["cost_currency"]}' not in receiver:
            return  await ctx.send(embed=simple_embed(False, "you have no money"))
        if receiver[f'balance{found_offer["cost_currency"]}'] < found_offer["cost_amount"]:
            return  await ctx.send(embed=simple_embed(False,"you don't have enough money"))
        sender =  guild_collection.find_one({"id":found_offer["person"]})
        if "wallet" in found_offer:
            if f'balance{found_offer["offer_currency"]}' not in sender:
                guild_collection.delete_one({"message_id":found_offer["message_id"]})
                return  await ctx.send(embed=simple_embed(False, "offer deleted, person does not have enough for trade"))
            if sender[f'balance{found_offer["offer_currency"]}'] < found_offer["offer_amount"]:
                guild_collection.delete_one({"message_id":found_offer["message_id"]})
                return  await ctx.send(embed=simple_embed(False, "offer deleted, person does not have enough for trade"))
        guild_collection.update_one(
            {"id":  receiver["id"] },
            { "$inc":{f'balance{found_offer["offer_currency"]}':-int(found_offer["offer_amount"])} }
        )
        guild_collection.update_one(
            {"id":  receiver["id"] },
            { "$inc":{f'balance{found_offer["cost_currency"]}':int(found_offer["cost_amount"])} }
        )
        if" wallet" in  found_offer:
            guild_collection.update_one(
                {"id":  sender["id"] },
                { "$inc":{f'balance{found_offer["offer_currency"]}':int(found_offer["offer_amount"])} }
            )
            guild_collection.update_one(
                {"id":  sender["id"] },
                { "$inc":{f'balance{found_offer["cost_currency"]}':-int(found_offer["cost_amount"])} }
            )
        if re.match(r'<@&?\d{18}>', found_offer["offer_currency"]) is not None:
            try:
                loop = asyncio.get_event_loop()
                id_role= re.findall(r'\d{18}', found_offer["offer_currency"])[0]
                print(id_role)
                id_role=int(id_role)
                role = discord.utils.get(guild.roles, id=id_role)
                print(role)
                loop.create_task(person.add_roles(role))
            except:
                return  await ctx.send(embed=simple_embed(False,"bad permissions"))
        if "uses" in found_offer:
            guild_collection.update_one(
                {"message_id":  found_offer["message_id"] },
                { "$inc":{"uses":-1} }
            )
        return  await ctx.send(embed=simple_embed(True,"success"))

    @commands.command(
        name='view-market',
        description='see all trades on the market right now',
        aliases=['vmar']
    )
    async def view_market(self, ctx):
        guild_collection =db[str(ctx.guild.id)]
        return_string=""
        offers=list(guild_collection.find({"type":"trade"}))
        for offer in offers:
            del offer["_id"]
            return_string+=f'{str(offer)}\n'
        return await ctx.send(embed=simple_embed(True, return_string[0:2000]))
    @commands.command(
        name='delete-all-trades',
        description='delete all trades currently on the market',
        aliases=['deltrades']
    )
    async def delete_all_trades(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send(embed=simple_embed(False,"must be admin"))
        guild_collection =db[str(ctx.guild.id)]
        guild_collection.delete_many({"type":"trade"})
        await ctx.send(embed=simple_embed(True, "all trades deleted"))
    @commands.command(
        name='inspect-trade',
        description='get info on a trade',
        aliases=['insp']
    )
    async def ispect_trade(self,ctx, id:int):
        guild_collection =db[str(ctx.guild.id)]
        print(id)
        trade= guild_collection.find_one({"type":"trade","message_id":id})
        if trade is None:
            return await ctx.send(embed=simple_embed(False, "cannot find that trade"))
        embedVar = discord.Embed(
            title="EU Economy Bot",
            color=0x00ff00,
            url=config["website"]
        )
        if "_id" in trade:
            del trade["_id"]
        if not "uses" in trade:
            trade["uses"]="(no usage limit set for this trade)"
        if not "offer_time" in trade:
            trade["offer_time"]="(no time limit set for this trade)"
        if not "people_restrictions" in trade:
            trade["people_restrictions"]="(no persoal limit set for this trade)"
        for attribute in trade:
            print(attribute, "name")
            if trade[attribute] is None or trade[attribute]=="":
                trade[attribute] ="(none)"
            print(trade[attribute], "value")
            embedVar.add_field(name=attribute,value=trade[attribute])
        return await ctx.send(embed=embedVar)
        
def setup(bot):
    bot.add_cog(Market(bot))



