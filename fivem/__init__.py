from redbot.core.bot import Red
from .fivem import FiveM


def setup(bot: Red):
    cog = FiveM(bot)
    bot.add_cog(cog)
