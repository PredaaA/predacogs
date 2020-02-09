from .randimages import RandImages


async def setup(bot):
    cog = RandImages(bot)
    bot.add_cog(cog)
