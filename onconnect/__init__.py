from redbot.core.bot import Red

from .onconnect import OnConnect

__red_end_user_data_statement__ = (
    "This cog does not persistently store data about users."
)


def setup(bot: Red) -> None:
    bot.add_cog(OnConnect(bot))
