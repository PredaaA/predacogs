from .randimages import RandImages

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)


async def setup(bot):
    cog = RandImages(bot)
    bot.add_cog(cog)
