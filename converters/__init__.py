from redbot.core.bot import Red
from .converters import Converters


def setup(bot: Red):
    cog = Converters(bot)
    bot.add_cog(cog)
