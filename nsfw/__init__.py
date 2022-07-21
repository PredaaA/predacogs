from redbot.core.bot import Red
from .nsfw import Nsfw

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)


async def setup(bot: Red):
    cog = Nsfw(bot)
    await bot.add_cog(cog)
