"""
MIT License

Copyright (c) 2019-2021 Predä

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

from __future__ import annotations

from typing import Union

from redbot.core import Config
from redbot.core.bot import Red


__all__ = ["SettingCacheManager"]


class SettingCacheManager:
    def __init__(self, bot: Red, config: Config, enable_cache: bool = True) -> None:
        self.__config: Config = config
        self.__bot: Red = bot
        self.enabled = enable_cache
        self._topgg_cache: Union[bool, Ellipsis] = ...
        self._detailed: Union[bool, Ellipsis] = ...
        self._lightmode: Union[bool, Ellipsis] = ...

    async def get_set_topgg(self, set_to: Union[bool, Ellipsis] = ...) -> bool:
        if set_to is ...:
            if self._topgg_cache is ...:
                self._topgg_cache = await self.__config.topgg_stats()
            return self._topgg_cache
        await self.__config.topgg_stats.set(set_to)
        self._topgg_cache = set_to
        return set_to

    async def get_set_detailed(self, set_to: Union[bool, Ellipsis] = ...) -> bool:
        if set_to is ...:
            if self._detailed is ...:
                self._detailed = await self.__config.detailed()
            return self._detailed
        await self.__config.detailed.set(set_to)
        self._detailed = set_to
        return set_to

    async def get_set_lightmode(self, set_to: Union[bool, Ellipsis] = ...) -> bool:
        if set_to is ...:
            if self._lightmode is ...:
                self._lightmode = await self.__config.lightmode()
            return self._lightmode
        await self.__config.lightmode.set(set_to)
        self._lightmode = set_to
        return set_to
