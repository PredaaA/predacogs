from .dbltools import DblToolsLite


def setup(bot):
    cog = DblToolsLite(bot)
    bot.add_cog(cog)
