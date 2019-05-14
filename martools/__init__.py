from .marttools import MartTools

def setup(bot):
    n = MartTools(bot)
    bot.add_cog(n)