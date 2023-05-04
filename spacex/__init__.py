from redbot.core.bot import Red
from .spacex import SpaceX

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)


async def setup(bot: Red):
    cog = SpaceX(bot)
    await bot.add_cog(cog)
