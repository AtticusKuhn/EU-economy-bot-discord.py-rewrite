from discord.ext import commands
import re

import os
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

import methods
from discord_utils.embeds import simple_embed
from config import config

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='set-config',
        description='allow admins to change the server settings',
        aliases=['s-c']
    )
    async def set_config(self, ctx, wallet,setting_name, option):
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


def setup(bot):
    bot.add_cog(Config(bot))
