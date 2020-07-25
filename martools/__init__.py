from redbot.core.bot import Red
from .marttools import MartTools


def setup(bot: Red):
    cog = MartTools(bot)
    bot.add_cog(cog)
