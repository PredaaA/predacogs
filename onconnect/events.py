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
from datetime import datetime, timezone

import discord
import psutil
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_timedelta

from .abc import MixinMeta


class Events(MixinMeta):
    """The listeners for shard events are found here."""

    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id: int) -> None:
        emoji = await self.config.orange()
        message = f"{emoji} Shard #{shard_id + 1}/{self.bot.shard_count} connected!"
        await self.bot.wait_until_red_ready()
        await self.send_event_message(message=message, colour=discord.Colour.orange())

    @commands.Cog.listener()
    async def on_shard_ready(self, shard_id: int) -> None:
        emoji = await self.config.green()
        message = f"{emoji} Shard #{shard_id + 1}/{self.bot.shard_count} ready!"
        await self.bot.wait_until_red_ready()
        await self.send_event_message(message=message, colour=discord.Colour.green())

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard_id: int) -> None:
        emoji = await self.config.red()
        message = f"{emoji} Shard #{shard_id + 1}/{self.bot.shard_count} disconnected!"
        await self.send_event_message(message=message, colour=discord.Colour.red())

    @commands.Cog.listener()
    async def on_shard_resumed(self, shard_id: int) -> None:
        emoji = await self.config.orange()
        message = f"{emoji} Shard #{shard_id + 1}/{self.bot.shard_count} resumed!"
        await self.bot.wait_until_red_ready()
        await self.send_event_message(message=message, colour=discord.Colour.orange())

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.bot.wait_until_red_ready()
        process_start = datetime.fromtimestamp(
            psutil.Process().create_time(), tz=timezone.utc
        )
        launch_time = humanize_timedelta(
            timedelta=datetime.now(tz=timezone.utc) - process_start
        )
        message = (
            f"> Launch time: {launch_time}\n\n{self.bot.user.name} is ready to use!"
        )
        await self.send_event_message(message=message, colour=discord.Colour.green())
