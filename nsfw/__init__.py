from redbot.core.bot import Red
from .nsfw import Nsfw


def setup(bot: Red):
    cog = Nsfw(bot)
    bot.add_cog(cog)
