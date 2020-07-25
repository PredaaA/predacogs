from redbot.core.bot import Red
from .whoplays import WhoPlays

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)


def setup(bot: Red):
    cog = WhoPlays(bot)
    bot.add_cog(cog)
