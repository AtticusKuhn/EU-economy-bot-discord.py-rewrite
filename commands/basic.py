from discord.ext import commands
from datetime import datetime as d
from discord_utils.embeds import simple_embed
import methods
import discord 
from config import config

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='ping',
        description='The ping command. Tests server lag',
        aliases=['p']
    )
    async def ping_command(self, ctx):
        start = d.timestamp(d.now())
        msg = await ctx.send(content='Pinging')
        await msg.edit(content=f'Pong!\nOne message round-trip took {(d.timestamp(d.now())-start) * 1000}ms.')
        return
    @commands.command(
        name='oldhelp',
        description='gives a list of possible commands',
        aliases=['oldcommands']
    )
    async def help(self, ctx, cog=""):
        if cog=="":
            return await ctx.send(embed=simple_embed(True,'''
    - $help - shows all commands
    - $send (from wallet) (to wallet) (amount) - sends an amount to a person from that wallet
    - $print (wallet name) (amount) - creates an amount of money in that wallet if you have the role "printer"
    - $balance (wallet name) - returns the amount of money in the wallet
    - $links - show some links related to this bot
    - $smart-contract (trigger) (code block) - code a smart contract
    - $clear-contracts - delete all your smart contracts.
    - $create (ping wallet) - create an account
    - $whois (condition) - figure out who is a condition
    - $send-each (from wallet) (ammount) (condition) - send each person who meets a condition
    - $set-balance (ping wallet) - set the balance of a wallet for admins only
    - $set-balance-each (amount) (condition) - set the balance of each person who meets a condition
    - $wallet-settings (target person) (ping wallet) (setting name) (boolean) - change the setting, such as view or access, to allow certain people to do more with wallets
    - $trade (wallet) (wanted currency) (giving up currency) (optional limitations) - create a trade
    - $accept (message id of trade) (wallet) - accept a trade
    - $quiz - start a quiz based on a subject
    - $shop (item name) (price) - same as trade but only for admins and you can also offer roles as trades
    - $work - get an amount of money no strings attached
    - $work-conditional (level name) (work reward) (conditional) - allows admins to add levels to working and give different people different work rewards       
            '''))
        if not cog in self.bot.cogs:
            return await ctx.send(embed=simple_embed(False,f'Unrecognized module. The recognized modules are {", ".join(self.bot.cogs)}'))
        return_commands = []
        for command in self.bot.commands:
            print("command",command.cog.__class__.__name__)
            if command.cog.__class__.__name__ == cog:
                return_commands.append(command)
        return_commands=list(map(lambda c:f'{str(c)} - {str(c.description)}',return_commands))
        return await ctx.send(embed=simple_embed(True,"\n".join(return_commands)))

    @commands.command(
        name='info',
        description='gives info on a secpfic command',
        aliases=['information', 'i']
    )
    async def info(self, ctx, command_name):
        command = [c for c in self.bot.commands if c.name==command_name]
        if len(command)>0:
            command=command[0]
           # attributes= [a for a in dir(command) if not a.startswith('__')]
           # embedVar = discord.Embed(
           #     title="EU Economy Bot",
           #     color=0x00ff00,
           #     url=config["website"]
           # )
            #print("attributes is", attributes)
            #for attr in attributes:
            #    value_string=str(getattr(command,attr))
            #    if value_string=="":
            #        value_string="(none)"
            #    embedVar.add_field(name=attr, value= value_string)
            #return await ctx.send(embed=embedVar)
            return await ctx.send(embed=simple_embed(True,f'name: {command.name}\n description:{command.description}\n aliases:{", ".join(command.aliases)}'))
        return await ctx.send(embed=simple_embed(False,"can't find command"))
    @commands.command(
        name='links',
        description='Show relevant links to this bot',
        aliases=['li']
    )
    async def links(self, ctx):
        return await ctx.send(embed=simple_embed("info","Github - https://github.com/eulerthedestroyer/EU-Economy-Bot \n Discord link -  https://discord.gg/ghFs7ZM \n Bot link - https://discord.com/api/oauth2/authorize?client_id=716434826151854111&permissions=268503104m&scope=bot \n Web interface - https://economy-bot.atticuskuhn.repl.co"))
    @commands.command(
        name='all-commands',
        description='gives a list of all implemented commands',
        aliases=['a-c',"help", "commands"]
    )
    async def all_commands(self, ctx):
        return_string=" ".join(list(map(lambda command: f'${str(command)} - {str(command.description)}\n', self.bot.commands)))
        return_string+='\n remember that to see commands relating to a specific module, you can do help {module name}. \n also to get info on a command do info {command name}'
        return await ctx.send(embed=simple_embed(True, return_string))
    @commands.command(
        name='whois',
        description='see who satisifies a given condition',
        aliases=['who']
    )
    async def whois(self, ctx, *condititons):
        people = methods.whois(condititons, ctx.guild)
        return_statement = ""
        symbol = "\n"
        if len(people)> 7:
            symbol = ","
        for index,person in enumerate(people):
            if len(return_statement) > 700:
                return_statement += f' and {len(people)-index} others'
                break
            return_statement = return_statement + f'<@{person}>{symbol}'
        if return_statement == "":
            return_statement = "(no people found)"
        embedVar = discord.Embed(title="Result", description=f'Found {len(people)} People', color=0x00ff00)
        embedVar.add_field(name="People", value=return_statement, inline=False)
        await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(Basic(bot))