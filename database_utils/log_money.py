import discord
import asyncio

import os
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

from discord_utils.embeds import simple_embed

def log_money(guild, message):
    print("log_money called")
    guild_collection = db[str(guild.id)]
    server_config =  guild_collection.find_one({
        "type":"server",
        "id"  : guild.id
    })
    if server_config is None:
        return
    print("config is not none")
    if "log-channel" not in server_config:
        return
    if server_config["log-channel"] is None:
        return
    print("log-channel exists and it is", server_config["log-channel"])
    channel = discord.utils.find(lambda m: str(m.id) == str(server_config["log-channel"]), guild.channels)
    if channel is None:
        return
    print("found channel")
    #asyncio.run(channel.send(f'log: {message}'))
    try:
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.create_task(channel.send(embed=simple_embed(True,f'log: {message}')))
