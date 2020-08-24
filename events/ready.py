import replit
from os import listdir
from os.path import isfile, join
cogs = list(map(lambda x: x[:-3],[f for f in listdir("commands") if isfile(join("commands", f))]))

async def ready(bot):
    replit.clear()
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    bot.remove_command('help')
    # Removes the help command
    # Make sure to do this before loading the cogs
    for cog in cogs:
        print("cog is",cog)
        bot.load_extension(f'commands.{cog}')
    return