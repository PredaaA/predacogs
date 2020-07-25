from redbot.core.bot import Red
from .dbltools import DblToolsLite


def setup(bot: Red):
    cog = DblToolsLite(bot)
    bot.add_cog(cog)
