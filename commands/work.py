from discord.ext import commands
import time
from config import config
import random
import re
import discord

import os
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URL"))
db = client.database

import methods
from discord_utils.embeds import simple_embed
from quiz import subject_to_quiz


class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='work',
        description='gain an amount of money',
        aliases=['w']
    )
    async def work(self, ctx):
        guild=ctx.guild
        person=ctx.author
        wallet = methods.find_create(person.id,guild)
        cooldown = config["work-cooldown"]
        guild_collection=db[str(guild.id)]

        server_config =  guild_collection.find_one({
            "type":"server","id"  : guild.id
        })
        if server_config is not None:
            if "work-cooldown" in server_config:
                cooldown = server_config["work-cooldown" ]
        if "cooldown-work" in wallet:
            print(time.time(), wallet["cooldown-work"],time.time() - wallet["cooldown-work"], cooldown)
            if time.time() - wallet["cooldown-work"] < cooldown:
                return  await ctx.send(embed=simple_embed(False,f'wait to work. You must wait {methods.seconds_to_time(cooldown- time.time()+wallet["cooldown-work"])} to work again'))
        payout =[{
            "name":"Bot default",
            "amount":config["work-payoff"]
        }]
        if server_config is not None:
            if "work-payoff" in server_config:
                payout[0] = {
                    "name":"server default",
                    "amount":server_config["work-payoff" ]
                }
            if "work-conditional" in server_config:
                payout += server_config["work-conditional"]
        parsed_message=""
        for index in payout:
            if "condition" in index:
                print(index["condition"])
                if person.id not in methods.whois(index["condition"].split(" "), guild):
                    print(person.id, methods.whois(index["condition"].split(" "), guild),person.id not in methods.whois(index["condition"].split(" "), guild) )
                    continue
            amount= index["amount"]
            if "-" in str(amount):
                amount=str(amount)
                currency=f'-{amount.split("-")[1]}'
                amount =int(amount.split("-")[0])
            else:
                currency=""
                amount=int(amount)
            guild_collection.update_one(
                {"id":  person.id },
                { "$inc":{f'balance{currency}':amount} }
            )
            parsed_message+= f'\n {index["amount"]} from {index["name"]}'

        guild_collection.update_one(
            {"id":  person.id },
            { "$set":{f'cooldown-work':time.time()} }
        )
        lines = open('data/jobs.txt').read().splitlines()
        job =random.choice(lines)
        return await ctx.send(embed=simple_embed(True,f'You worked as {job} and earned {parsed_message}'))
    @commands.command(
        name='work-conditional',
        description='allow admins to set different work amounts for different roles',
        aliases=['w-c']
    )
    async def work_conditions(self, ctx ,level_name, amount, *conditional):
        if not ctx.author.guild_permissions.adminsitrator:
            return await ctx.send(embed=simple_embed(False, "must be admin"))
        guild=ctx.guild
        guild_collection=db[str(guild.id)]
        server_config =  guild_collection.find_one({
            "type":"server","id"  : guild.id
        })
        if server_config is None:
            guild_collection.insert_one({
                "type":"server",
                "id":guild.id,
                "default_balance": config["default_balance"]
            })
            server_config =  guild_collection.find_one({
                "type":"server","id"  : guild.id
            })
        if not re.match(r"^\d+(-[a-z]{3,10})?$", amount):
            return await ctx.send(embed=simple_embed(False, "Invlaid currency"))
        if not re.match(r"^\w{3,10}$", level_name):
            return await ctx.send(embed=simple_embed(False, "Invlaid level name"))
        guild_collection.update_one(
            {"id":guild.id},
            {"$push":{f'work-conditional':{
                "name":level_name,
                "condition":" ".join(conditional),
                "amount":amount
            }}}
        )
        return await ctx.send(embed=simple_embed(True, "work level set"))
    @commands.command(
        name='quiz',
        description='take a quiz for a cash prize',
        aliases=['qz']
    )       
    async def get_question(self, ctx):
        guild=ctx.guild
        person=ctx.author

        guild_collection=db[str(guild.id)]
        server_config =  guild_collection.find_one({
            "type":"server",
            "id"  : guild.id
        })
        if server_config is None:
            return await ctx.send(embed=simple_embed (False, "server config is not set up. Ask your admin to set up the config"))
        quiz_cooldown = config["quiz-cooldown"]
        if "quiz-cooldown" in server_config:
            quiz_cooldown = server_config["quiz-cooldown"]
        person_wallet = guild_collection.find_one({"id":person.id})
        if person_wallet is not None:
            if "quiz-cooldown" in person_wallet:
                if time.time() - person_wallet["quiz-cooldown"] <quiz_cooldown:
                    return await ctx.send(embed=simple_embed (False,f'wait to quiz. You must wait {methods.seconds_to_time(quiz_cooldown- time.time()+person_wallet["quiz-cooldown"])} to quiz again'))
        guild_collection.update_one(
            {"id":person.id},
            {"$set":{"quiz-cooldown":time.time()}}
        )
        if not "quiz-subject" in server_config:
            return await ctx.send(embed=simple_embed (False, "no quiz subject for this server set. Ask you admin to set the quiz subject by doing something like $config quiz-subject {Subject}"))
        await ctx.send(embed=simple_embed ("info", "Parsing sentence to generate question....."))
        question = subject_to_quiz(server_config["quiz-subject"])
        print(question,"question")
        guild_collection.insert_one({
            "type":"quiz",
            "person":person.id,
            "question":question,
            "time":time.time()
        })
        return await ctx.send(embed=simple_embed (True, question["question"]))
    @commands.command(
        name='see-work-levels',
        description='look at all work levels',
        aliases=['swl']
    )       
    async def see_work_levels(self, ctx):
        guild=ctx.guild
        person=ctx.author
        guild_collection=db[str(guild.id)]
        server_config =  guild_collection.find_one({
            "type":"server","id"  : guild.id
        })
        print("server config is", server_config)
        if server_config is None:
            return await ctx.send(embed=simple_embed(False,"can't find the work conditional"))
        embedVar = discord.Embed(
            title="EU Economy Bot",
            color=0x00ff00,
            url=config["website"]
        )
        if "work-payoff" in server_config:
            embedVar.add_field(name="work payoff", value= server_config["work-payoff"])
        if "work-conditional" in server_config:
            for condition in server_config["work-conditional"]:
                print("condition is", condition)
                embedVar.add_field(name=condition["name"], value=condition["condition"])
        return await ctx.send(embed=embedVar)
    @commands.command(
        name='delete work leve;',
        description='delete a work level by name',
        aliases=['dwl']
    )
    @commands.has_permissions(administrator=True)       
    async def delete_work(self, ctx, conditional_name):
        guild_collection=db[str(ctx.guild.id)]
        server_config =  guild_collection.find_one({
            "type":"server","id"  : ctx.guild.id
        })
        print("server config is", server_config)
        if server_config is None:
            return await ctx.send(embed=simple_embed(False,"can't find the work conditional"))
        if not "work-conditional" in server_config:
            return await ctx.send(embed=simple_embed(False,"can't find the work conditional"))
        matches = [x for x in server_config["work-conditional"] if x["name"]!=conditional_name]
        if len(matches) ==len(server_config["work-conditional"]):
            return await ctx.send(embed=simple_embed(False,"can't find the work conditional by that given name"))
        guild_collection.update_one(
            {"id":ctx.guild.id},
            {"$set":{f'work-conditional': matches }}
        )
        return await ctx.send(embed=simple_embed(True,"ok it was deleted"))

def setup(bot):
    bot.add_cog(Work(bot))


def answer_question(ctx, answer):
    guild=ctx.guild
    person=ctx.author
    guild_collection=db[str(guild.id)]
    question = guild_collection.find_one({"type":"quiz","person":person.id})
    if question is None:
        return None
    guild_collection.delete_one({"type":"quiz","person":person.id})
    server_config =  guild_collection.find_one({
        "type":"server",
        "id"  : guild.id
    })
    quiz_time = config["quiz-time"]
    if "quiz-time" in server_config:
        quiz_time = server_config["quiz-time"]
    if time.time() - question["time"] >quiz_time:
        return (False, "you ran out of time sorry")
    if question["question"] is not None:
        if "answer" in  question["question"]:
            if question["question"]["answer"].lower() != answer.lower() and answer not in question["question"]["similar_words"]:
                return (False,f'incorrect answer, correct answer is {question["question"]["answer"]}')
    if server_config is not None and "quiz-payoff" in server_config:
        guild_collection.update_one(
            {"id":  person.id },
            { "$inc":{f'balance':server_config["quiz-payoff"]} }
        )
        return (True, f'your balance has been increased by {server_config["quiz-payoff"]}')

    guild_collection.update_one(
        {"id":  person.id },
        { "$inc":{f'balance':1} }
    )
    if answer in question["question"]["similar_words"]:
        return (True, f'the correct answer was {question["question"]["answer"]}, but that was close enough to be correct.')
    return (True, "your balance has been increased by one")
