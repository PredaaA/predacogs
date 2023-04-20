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
from abc import ABC, abstractmethod
from typing import Optional, Union

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red


class MixinMeta(ABC):
    __author__: str
    __version__: str

    def __init__(self, *_args) -> None:
        self.bot: Red
        self.config: Config

    @staticmethod
    @abstractmethod
    async def maybe_reply(
        ctx: commands.Context,
        message: Optional[str] = None,
        embed: Optional[discord.Embed] = None,
        mention_author: Optional[bool] = False,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_or_fetch_channel(self, channel_id: int):
        raise NotImplementedError()

    @abstractmethod
    async def send_event_message(
        self, message: str, colour: Union[discord.Colour, int]
    ) -> None:
        raise NotImplementedError()
