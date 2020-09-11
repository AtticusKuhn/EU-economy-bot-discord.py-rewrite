from discord.ext import commands
import re

import os
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

import methods
from discord_utils.embeds import simple_embed, dict_to_embed
from config import config

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='set-config',
        description='allow admins to change the server settings',
        aliases=['s-c']
    )
    async def set_config(self, ctx,setting_name, option):
        guild = ctx.guild
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send(embed=simple_embed(False,"must be admin"))
        guild_collection =db[str(guild.id)]
        server_config =  guild_collection.find_one({
            "type":"server",
            "id"  : guild.id
        })
        if server_config is None:
            guild_collection.insert_one({
                "type":"server",
                "id":guild.id,
                "default_balance": config["default_balance"]
            })
        if setting_name in ["default_balance","quiz-payoff", "quiz-cooldown","work-payoff","work-cooldown","quiz-time"]:
            if not option.isdigit():
                return await ctx.send(embed=simple_embed (False, "must be a number"))
            option=int(option)
        
        if setting_name not in config["config_options"]:
            return await ctx.send(embed=simple_embed (False, f'cannot find hat setting; Currently supported settings are ${", ".join(config["config_options"].keys())} '))
        if setting_name == "log-channel":
            match = re.match(r'<#\d{18}>', option)
            print(match)
            if match is None:
                return await ctx.send(embed=simple_embed(False, "invalid channel"))
            option = re.findall(r'\d{18}', option)[0]
            print(option)
        guild_collection.update_one({
        '_id': server_config['_id']
        },{
            '$set': {
            setting_name :option
            }
        })
        return await ctx.send(embed=simple_embed( True, "success"))
    @commands.command(
        name='view-config',
        description='see what the current server config is ',
        aliases=['v-c']
    )
    async def view_config(self, ctx):
        guild = ctx.guild
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send(embed=simple_embed(False,"must be admin"))
        guild_collection =db[str(guild.id)]
        server_config =  guild_collection.find_one({"type":"server","id"  : guild.id})
        if server_config is None:
            guild_collection.insert_one({
                "type":"server",
                "id":guild.id,
                "default_balance": config["default_balance"]
            })
        server_config =  guild_collection.find_one({"type":"server","id"  : guild.id})
        del server_config["_id"]
        return await ctx.send(embed=dict_to_embed( server_config))
    @commands.command(
        name='prune',
        description='delete all wallets that no longer exist ',
        aliases=['pr']
    )
    @commands.has_permissions(administrator=True)       
    async def prune(self, ctx):
        guild_collection =db[str(ctx.guild.id)]
        all_wallets= guild_collection.find({})
        return_message=""
        deleting = []
        for wallet in all_wallets:
            if "type" in wallet:                
                if wallet["type"]=="personal" or wallet["type"]=="role":
                    #print("trying", wallet["name"])
                    found = methods.get_wallet(ctx.guild,str(wallet["id"]))
                    #print("found is ", found)
                    if not found[0]:
                        return_message+=f'\n deleted {wallet["name"]}'
                        deleting.append(wallet["_id"])
               # if :
               #     print("trying", wallet["name"])
               #     if wallet["type"]=="personal":
               #         if not  methods.get_wallet(ctx.guild, str(wallet["id"]))[0]:
               #             return_message+=f'\n deleted {wallet["name"]}'
        guild_collection.remove({'_id':{'$in':deleting}})
        if return_message=="":
            return_message="deleted no one"
        return await ctx.send(embed=simple_embed( True, return_message))
        
def setup(bot):
    bot.add_cog(Config(bot))
