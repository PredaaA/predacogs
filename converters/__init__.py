from .converters import Converters

def setup(bot):
    n = Converters(bot)
    bot.add_cog(n)