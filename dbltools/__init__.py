from .dbltools import DblTools

async def setup(bot):
    n = DblTools(bot)
    await n.initialize()
    bot.add_cog(n)