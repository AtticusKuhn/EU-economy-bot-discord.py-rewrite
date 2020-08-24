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

class Smart_contract(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(Smart_contract(bot))