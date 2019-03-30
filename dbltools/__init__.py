from .dbltools import DblTools

def setup(bot):
    n = DblTools(bot)
    bot.add_cog(n)