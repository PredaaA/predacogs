from .whoplays import WhoPlays

def setup(bot):
    n = WhoPlays(bot)
    bot.add_cog(n)