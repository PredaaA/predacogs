"""
MIT License

Copyright (c) 2022-2023 ltzmax
Copyright (c) 2023-present PredaaA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import logging
from abc import ABC
from typing import Optional, Union

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red

from .commands import Commands
from .events import Events

log = logging.getLogger("red.maxcogs.onconnect")


class CompositeMetaClass(type(commands.Cog), type(ABC)):
    """
    This allows the metaclass used for proper type detection to
    coexist with discord.py's metaclass
    """

    pass


class OnConnect(Events, Commands, commands.Cog, metaclass=CompositeMetaClass):
    """This cog is used to send shard events."""

    __version__ = "0.1.18"
    __author__ = "MAX"

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=0x345628097929936898, force_registration=True
        )
        default_global = {
            "statuschannel": None,
            "green": "\N{LARGE GREEN CIRCLE}",
            "orange": "\N{LARGE ORANGE CIRCLE}",
            "red": "\N{LARGE RED CIRCLE}",
        }
        self.config.register_global(**default_global)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre = super().format_help_for_context(ctx)
        return f"{pre}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"

    async def red_get_data_for_user(self, *, user_id: int) -> dict:
        """This cog does not story any end user data."""
        return {}

    async def red_delete_data_for_user(self, **kwargs) -> None:
        """Nothing to delete."""
        return

    @staticmethod
    async def maybe_reply(
        ctx: commands.Context,
        message: Optional[str] = None,
        embed: Optional[discord.Embed] = None,
        mention_author: Optional[bool] = False,
    ) -> None:
        """Try to reply to a message.

        Parameters
        ----------
        ctx : redbot.core.commands.Context
            The command invocation context.

        message : Optional[str] = None
            The message to send.

        embed : Optional[discord.Embed] = None
            The embed to send in the message.

        mention_author : Optional[bool] = False
            Whether to mention the author of the message. Defaults to False.
        """
        try:
            await ctx.reply(message, embed=embed, mention_author=mention_author)
        except discord.HTTPException:
            await ctx.send(message, embed=embed)

    # Based on https://github.com/Cog-Creators/Red-DiscordBot/blob/9ab307c1efc391301fc6498391d2e403aeee2faa/redbot/core/bot.py#L925 # noqa
    async def get_or_fetch_channel(self, channel_id: int):
        """Retrieves a channel based on its ID.

        Parameters
        -----------
        channel_id: int
            The id of the channel to retrieve.
        """
        if (channel := self.bot.get_channel(channel_id)) is not None:
            return channel

        return await self.bot.fetch_channel(channel_id)

    async def send_event_message(
        self, message: str, colour: Union[discord.Colour, int]
    ) -> None:
        """Send an embed message to the set statuschannel.

        Parameters
        -----------
        message: str
            The message to send to the statuschannel.

        colour: Union[discord.Colour, int]
            The colour to set in the embed message.
        """
        channel_config = await self.config.statuschannel()
        if channel_config is None:
            return

        try:
            channel = await self.get_or_fetch_channel(channel_id=channel_config)
        except discord.NotFound as e:
            if await self.config.statuschannel() is not None:
                await self.config.statuschannel.clear()
                log.error(f"Statuschannel not found, deleting ID from config. {e}")

            return

        event_embed = discord.Embed(description=message, colour=colour)
        embed_channel = await channel.send(embed=event_embed)
