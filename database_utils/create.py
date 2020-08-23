import os
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

import methods
from config import config

def create(guild, wallet_ping):
    print("created called with", wallet_ping)
    guild_collection =db[str(guild.id)]
    get_wallet_result = methods.get_wallet( guild, wallet_ping)
    
    #print(get_wallet_result)
    server_config =  guild_collection.find_one({
            "type":"server",
            "id"  : guild.id
    })
    if server_config is not None:
        default_balance =server_config["default_balance"]
    else:
        guild_collection.insert_one({
            "type":"server",
            "id":guild.id,
            "default_balance": config["default_balance"]
        })
        default_balance = config["default_balance"]
    if(get_wallet_result[0]):
        if guild_collection.find_one({ "id":get_wallet_result[1].id}):
            return (False, "account already exists")
        for person in guild.members:
            if(person.id == get_wallet_result[1].id):
                found_person = person
        for role in guild.roles:
            if(role.id == get_wallet_result[1].id):
                found_role = role
        if(get_wallet_result[2] == "person"):
            return_wallet = guild_collection.insert_one({
                "name"   :found_person.name,
                "id"     :found_person.id,
                "type"   :"personal",
                "balance": int(default_balance)
             })
            return_wallet = guild_collection.find_one({"id":return_wallet.inserted_id})
        else:
            return_wallet = guild_collection.insert_one({
                "name"   :found_role.name,
                "id"     :found_role.id,
                "type"   :"role",
                "balance": int(default_balance)
             })
            return_wallet = guild_collection.find_one({"_id":return_wallet.inserted_id})
        print("create will return", return_wallet)
        return (True, "created",return_wallet)
    else:
        return (False, "doesn't exist")