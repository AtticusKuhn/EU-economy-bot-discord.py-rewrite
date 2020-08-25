from discord_utils.embeds import simple_embed 
import traceback

async def command_error(ctx, error):
    print(error)
    await ctx.send(embed =simple_embed(False, str(error)))
    etype = type(error)
    trace = error.__traceback__
    verbosity = 4
    lines = traceback.format_exception(etype, error, trace, verbosity)
    traceback_text = ''.join(lines)
    print(traceback_text)
	