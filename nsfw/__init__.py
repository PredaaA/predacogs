from .nsfw import Nsfw

def setup(bot):
    n = Nsfw(bot)
    bot.add_cog(n)