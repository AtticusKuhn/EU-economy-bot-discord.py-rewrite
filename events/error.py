from discord_utils.embeds import simple_embed 
import traceback
from discord.ext.commands import CommandNotFound
import re
from Levenshtein import distance

async def command_error(bot, ctx, error):
    if isinstance(error, CommandNotFound):
        regex = re.search(r'"([A-Za-z0-9_\./\\-]*)"', str(error))
        false_command = regex.group()
        dis=1000
        current_command=""
        for command in bot.commands:
            test_distance = distance(command.name, false_command)
            if  test_distance< dis:
                #print(f'distance from {command.name} to {false_command} is {test_distance}')
                dis= test_distance
                current_command= command.name
            for alias in command.aliases:
                test_distance = distance(alias, false_command)
                #print(f'distance from {alias} to {false_command} is {test_distance}')
                if  test_distance< dis:
                    dis= test_distance
                    current_command= alias
        return await ctx.send(embed=simple_embed(False, f' I do not recognize that command. It is closest to "{current_command}"'))
    print(error, "error")
    await ctx.send(embed =simple_embed(False, str(error)))
    etype = type(error)
    trace = error.__traceback__
    verbosity = 4
    lines = traceback.format_exception(etype, error, trace, verbosity)
    traceback_text = ''.join(lines)
    print(traceback_text)
	