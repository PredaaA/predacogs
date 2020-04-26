from .dbltools import DblTools


def setup(bot):
    cog = DblTools(bot)
    bot.add_cog(cog)
