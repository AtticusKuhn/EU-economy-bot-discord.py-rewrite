from discord.ext import commands
import methods

class WalletConverter(commands.Converter):
    async def convert(self, ctx, wallet):
        if wallet is None:
            wallet=ctx.author.mention
        get_wallet_result = methods.get_wallet(ctx.guild, wallet)    
        if not get_wallet_result[0]:
            raise Exception("person does not exist in this guild")
        db_wallet = methods.find_create(get_wallet_result[1].id, ctx.guild)
        #print("db_wallet:", db_wallet)
        return db_wallet