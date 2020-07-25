from redbot.core.bot import Red
from .randimages import RandImages


async def setup(bot: Red):
    cog = RandImages(bot)
    bot.add_cog(cog)
