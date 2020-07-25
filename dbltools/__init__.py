from redbot.core.bot import Red
from .dbltools import DblTools


def setup(bot: Red):
    cog = DblTools(bot)
    bot.add_cog(cog)
