from .spacex import SpaceX


def setup(bot):
    n = SpaceX(bot)
    bot.add_cog(n)
