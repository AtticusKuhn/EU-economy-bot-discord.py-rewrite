from commands.work import answer_question
from discord_utils.embeds import simple_embed
from commands.smart_contract import execute_contracts

import os
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database


async def message(bot, ctx):
    if ctx.author.bot:
        return ## don't reply to other bots
    if not ctx.guild:
        return await ctx.channel.send(embed=simple_embed(False,"only work in a guild"))
    #print("message has been called")
    ###quiz
    answer = answer_question(ctx,ctx.content[1:])
    if answer is not None:
        await ctx.channel.send(embed=simple_embed(*answer))
    ###smart contracts
    guild_collection =db[str(ctx.guild.id)]
    message_contracts = guild_collection.find({"trigger":"message"})
    execution_result = execute_contracts(ctx.guild,message_contracts, ctx, "message" )
    #print(execution_result)
    for result in execution_result:
        if result is not None:
            await ctx.channel.send(embed=simple_embed(result[0],result[1]))
    await bot.process_commands(ctx)