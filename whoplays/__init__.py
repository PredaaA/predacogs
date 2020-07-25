from redbot.core.bot import Red
from .whoplays import WhoPlays


def setup(bot: Red):
    cog = WhoPlays(bot)
    bot.add_cog(cog)
