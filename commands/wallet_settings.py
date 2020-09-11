from config import config
from database_utils.wallet_converter import WalletConverter

import os
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

from discord.ext import commands
from discord_utils.embeds import simple_embed

class WalletSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='set-wallet-settings',
        description='change settings of a wallet',
        aliases=['sws']
    )
    async def set_settings(self, ctx, account:WalletConverter, setting_name, value):
        if not setting_name in config["wallet_settings"] and not setting_name.startswith("print-"):
            return await ctx.send(embed=simple_embed  (False, "invalid setting name"))
        value = (value.lower() == "true")
        person = ctx.author
        guild_collection =db[str(ctx.guild.id)]
        account =guild_collection.find_one({"id":account["id"]})
        if not account:
            return await ctx.send(embed=simple_embed  (False,"wallet does not have an accound"))
        can_access = False
        if person.guild_permissions.administrator:
            can_access = True
        if not can_access:
            return await ctx.send(embed=simple_embed  (False, "you cannot edit the settings of this wallet"))
        temp = account
        print(temp, setting_name)
        if not "permissions" in temp:
            temp["permissions"] = {
            }
        if temp["permissions"] is None:
            temp["permissions"] = {
            }
        if not setting_name in temp["permissions"]:
            temp["permissions"][setting_name] ={
                "true":[],
                "false":[]
            }
        if not "true" in temp["permissions"][setting_name]:
            temp["permissions"][setting_name] ={
                "true":[],
                "false":[]
            }
        if value:
            if account["id"] in temp["permissions"][setting_name]["true"]:
                return await ctx.send(embed=simple_embed  (False, "setting already true"))
            temp["permissions"][setting_name]["true"].append(account["id"] )
            try:
                temp["permissions"][setting_name]["false"].remove(account["id"] )
            except:
                pass
        else:
            if account["id"] in temp["permissions"][setting_name]["false"]:
                return await ctx.send(embed=simple_embed  (False, "setting already false"))
            temp["permissions"][setting_name]["false"].append(account["id"] )
            try:
                temp["permissions"][setting_name]["true"].remove(account["id"] )
            except:
                pass
        guild_collection.update_one(
            {"_id":account["_id"] },
            { "$set":{"permissions":temp["permissions"]}}
        )
        return (True, "settings successfully changed")

def setup(bot):
    bot.add_cog(WalletSettings(bot))