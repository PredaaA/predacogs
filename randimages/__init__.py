from redbot.core.bot import Red
from .randimages import RandImages

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)


async def setup(bot: Red):
    cog = RandImages(bot)
    bot.add_cog(cog)
