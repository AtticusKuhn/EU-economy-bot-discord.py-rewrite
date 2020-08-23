from discord_utils.embeds import simple_embed 

async def command_error(ctx, error):
    print(error)
    await ctx.send(embed =simple_embed(False, str(error)))
    print(error.__traceback__)
    '''if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Hey! I can't do this command unless you give me some perms!")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument!")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey! You do not have the required permissions to preform this command!")
    if isinstance(error, commands.TooManyArguments):
        await ctx.send("Too many arguments!")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command doesn't exist buddy. Refer to .help")
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command!")
    if isinstance(error, commands.CommandOnCooldown):
        if ctx.message.author.guild_permissions.manage_roles:
            await ctx.reinvoke()
            return
        await ctx.send(error)
    etype = type(error)
    trace = error.__traceback__
    verbosity = 4
    lines = traceback.format_exception(etype, error, trace, verbosity)
    traceback_text = ''.join(lines)
    print(traceback_text)'''
	