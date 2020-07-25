from redbot.core.bot import Red
from .spacex import SpaceX


def setup(bot: Red):
    cog = SpaceX(bot)
    bot.add_cog(cog)
