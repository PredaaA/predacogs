from redbot.core.bot import Red

from .onconnect import OnConnect

__red_end_user_data_statement__ = (
    "This cog does not persistently store data about users."
)


async def setup(bot: Red) -> None:
    await bot.add_cog(OnConnect(bot))
