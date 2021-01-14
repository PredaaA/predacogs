"""
MIT License

Copyright (c) 2020 Predä

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

import asyncio
import contextlib
import logging
from collections import Counter
from typing import List, Mapping

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS

from redbot.core.bot import Red
from redbot.core import commands, checks, Config
from redbot.core.utils import AsyncIter

from .setting_cache import SettingCacheManager
from .stats_task import start_stats_tasks, call_sync_as_async, init_bot_stats

log = logging.getLogger("red.predacogs.TimeSeries")


class TimeSeries(commands.Cog):
    """Get multiple stats of your bot sent to an InfluxDB instance."""

    # This cog is an adaptation of what Draper done first, my personal changes,
    # and other stuff that I've done for a bounty.

    __author__ = ["Draper#6666", "Predä 。#1001"]
    __version__ = "1.1.12"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=332980470202044161, force_registration=True)
        self.config.register_global(
            url="http://localhost:9999",
            bucket="bucket",
            org="org",
            commands_stats=Counter({}),
            detailed=True,
            topgg_stats=False,
            lightmode=False,
        )
        self.commands_cache = {"session": Counter(), "persistent": Counter()}
        self.config_cache = SettingCacheManager(bot=self.bot, config=self.config)

        self._tasks: List[asyncio.Task] = []
        init_bot_stats(self.bot)

        self.client = {"client": None, "bucket": None, "write_api": None}
        self.api_ready = False
        self._start_task = bot.loop.create_task(self.initialise())

    async def initialise(self):
        try:
            val = getattr(self.bot, "_stats_task", None)
            recreate = False
            if val is None:
                recreate = True
            elif val:
                if isinstance(val, asyncio.Task):
                    recreate = True
                    if not val.done():
                        val.cancel()
                else:
                    recreate = True
            if recreate:
                start_stats_tasks(self.bot, self.config_cache)
            await self.wait_until_stats_ready()
            await self.connect_to_influx()
            self.commands_cache["persistent"] = await self.config.commands_stats()
            await self.start_tasks()
        except Exception as err:
            log.exception("Exception in cog initialise", exc_info=err)

    async def wait_until_stats_ready(self):
        """Wait until stats task has done its first loop."""
        await self.bot._stats_ready.wait()

    def cog_unload(self):
        self.bot.loop.create_task(self.update_command_usage())
        if self._start_task:
            self._start_task.cancel()
        for task in self._tasks:
            with contextlib.suppress(Exception):
                task.cancel()

        if self.client["client"]:
            self.client["client"].__del__()
            self.client["write_api"].__del__()

        if getattr(self.bot, "_stats_task", None):
            self.bot._stats_task.cancel()

    async def connect_to_influx(self, token=None):
        if self.api_ready:
            self.client["client"].__del__()
            self.client["write_api"].__del__()
            self.client = {"client": None, "bucket": None, "write_api": None}
            self.api_ready = False

        config = await self.config.all()
        token = (
            token.get("api_key", "")
            if token
            else (await self.bot.get_shared_api_tokens("timeseries")).get("api_key", "")
        )
        client = call_sync_as_async(
            InfluxDBClient,
            url=config["url"],
            org=config["org"],
            token=token,
            enable_gzip=True,
            timeout=2,
        )
        if client.health().status == "pass":
            self.client = {
                "client": client,
                "bucket": config["bucket"],
                "write_api": client.write_api(write_options=ASYNCHRONOUS),
            }
            self.api_ready = True
        else:
            client.close()
        return self.api_ready

    @commands.Cog.listener()
    async def on_red_api_tokens_update(self, service_name: str, api_tokens: Mapping[str, str]):
        if service_name != "timeseries":
            return
        await self.connect_to_influx(api_tokens)

    async def update_command_usage(self):
        await self.config.commands_stats.set(self.commands_cache["persistent"])
        self.commands_cache["session"].clear()
        self.commands_cache["persistent"].clear()

    async def write_bot_data(self):
        if not self.api_ready:
            return
        try:
            unchunked_guilds = len(
                [
                    guild
                    async for guild in AsyncIter(self.bot.guilds, steps=25)
                    if not guild.chunked and not guild.unavailable and guild.large
                ]
            )
            p = Point("-")
            for k, v in self.bot.stats.bot.__dict__.items():
                if unchunked_guilds >= 8 and k == "Unique Users":
                    continue
                p.field(str(k), v)
            call_sync_as_async(
                self.client["write_api"].write, bucket=self.client["bucket"], record=p
            )

            p = Point("Server Region")
            for k, v in self.bot.stats.guilds_regions.__dict__.items():
                p.field(str(k), v)
            call_sync_as_async(
                self.client["write_api"].write, bucket=self.client["bucket"], record=p
            )

            p = Point("Servers")
            for k, v in self.bot.stats.guilds.__dict__.items():
                if unchunked_guilds >= 8 and k == "Members":
                    continue
                p.field(str(k), v)
            call_sync_as_async(
                self.client["write_api"].write, bucket=self.client["bucket"], record=p
            )

            p = Point("Server Features")
            for k, v in self.bot.stats.guild_features.__dict__.items():
                p.field(str(k), v)
            call_sync_as_async(
                self.client["write_api"].write, bucket=self.client["bucket"], record=p
            )

            p = Point("Server Verification")
            for k, v in self.bot.stats.guild_verification.__dict__.items():
                p.field(str(k), v)
            call_sync_as_async(
                self.client["write_api"].write, bucket=self.client["bucket"], record=p
            )
        except Exception as err:
            log.exception("Error while saving bot data to Influx", exc_info=err)

    async def write_audio_data(self):
        if not self.api_ready:
            return
        try:
            p = Point("Audio")
            for k, v in self.bot.stats.audio.__dict__.items():
                p.field(str(k), v)
            call_sync_as_async(
                self.client["write_api"].write, bucket=self.client["bucket"], record=p
            )
        except Exception as err:
            log.exception("Error while saving audio data to Influx", exc_info=err)

    async def write_shard_latencies_data(self):
        if not self.api_ready:
            return
        try:
            p = Point("Shard")
            for k, v in self.bot.stats.shards.__dict__.items():
                p.field(str(k), v)
            call_sync_as_async(
                self.client["write_api"].write, bucket=self.client["bucket"], record=p
            )
        except Exception as err:
            log.exception("Error while saving shard data to Influx", exc_info=err)

    async def write_currency_data(self):
        if not self.api_ready:
            return
        try:
            p = Point("-")
            for k, v in self.bot.stats.currency.__dict__.items():
                p.field(str(k), v)
            call_sync_as_async(
                self.client["write_api"].write, bucket=self.client["bucket"], record=p
            )
        except Exception as err:
            log.exception("Error while saving currency data to Influx", exc_info=err)

    async def write_commands_data(self):
        if not self.api_ready:
            return
        try:
            p = Point("Commands")
            for k, v in self.commands_cache["session"].items():
                p.field(str(k), v)
            call_sync_as_async(
                self.client["write_api"].write, bucket=self.client["bucket"], record=p
            )

            p = Point("Commands Persistent")
            for k, v in self.commands_cache["persistent"].items():
                p.field(str(k), v)
            call_sync_as_async(
                self.client["write_api"].write, bucket=self.client["bucket"], record=p
            )
        except Exception as err:
            log.exception("Error while saving command data to Influx", exc_info=err)

    async def write_adventure_data(self):
        if not self.api_ready:
            return
        if self.bot.get_cog("Adventure") is None:
            return
        try:
            p = Point("Adventure")
            for k, v in self.bot.stats.adventure.__dict__.items():
                p.field(str(k), v)
            call_sync_as_async(
                self.client["write_api"].write, bucket=self.client["bucket"], record=p
            )
        except Exception as err:
            log.exception("Error while saving adventure data to Influx", exc_info=err)

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        if not self.api_ready:
            return
        if ctx.message.author.bot:
            return
        command = ctx.command.qualified_name
        self.commands_cache["session"][command] += 1
        self.commands_cache["persistent"][command] += 1

    async def start_tasks(self):
        for task in [self.update_task, self.save_commands_stats]:
            self._tasks.append(self.bot.loop.create_task(task(self.bot)))

    async def run_events(self):
        await asyncio.gather(
            *[
                self.write_bot_data(),
                self.write_currency_data(),
                self.write_shard_latencies_data(),
                self.write_audio_data(),
                self.write_commands_data(),
                self.write_adventure_data(),
            ],
            return_exceptions=True,
        )

    async def update_task(self, bot):
        with contextlib.suppress(asyncio.CancelledError):
            while True:
                try:
                    await self.run_events()
                except asyncio.CancelledError:
                    break
                except Exception as exc:
                    log.exception("update_task", exc_info=exc)
                    await asyncio.sleep(15)
                else:
                    await asyncio.sleep(60)

    async def save_commands_stats(self, bot):
        with contextlib.suppress(asyncio.CancelledError):
            while True:
                await asyncio.sleep(1800)
                await self.config.commands_stats.set(self.commands_cache["persistent"])

    @checks.is_owner()
    @commands.group()
    async def timeseriesset(self, ctx: commands.Context):
        """
        Settings for InfluxDB API.
        
        Be sure to have an instance running. https://v2.docs.influxdata.com/v2.0/get-started/
        """

    @timeseriesset.command()
    async def url(self, ctx: commands.Context, *, url: str = "http://localhost:9999"):
        """Set the InfluxDB url. Default is `http://localhost:9999`."""
        if url.endswith("/"):
            url = url.rstrip("/")
        await self.config.url.set(url)
        connection = await self.connect_to_influx()
        await ctx.tick() if connection else await ctx.send(
            "Cannot connect to that URL. "
            "Please make sure that it is correct or to also set a bucket and organization name."
        )

    @timeseriesset.command()
    async def bucket(self, ctx: commands.Context, *, bucket: str = None):
        """Set the bucket name."""
        await self.config.bucket.set(bucket)
        connection = await self.connect_to_influx()
        await ctx.tick() if connection else await ctx.send(
            "Cannot connect with that bucket name. "
            "Please make sure that it is correct or to also set an URL and an organization name."
        )

    @timeseriesset.command()
    async def org(self, ctx: commands.Context, *, org: str = None):
        """Set the organization name."""
        await self.config.org.set(org)
        connection = await self.connect_to_influx()
        await ctx.tick() if connection else await ctx.send(
            "Cannot connect with that organization name. "
            "Please make sure that it is correct or to also set an URL and a bucket name."
        )

    @timeseriesset.command()
    async def token(self, ctx: commands.Context):
        """Instructions on how to set the token."""
        msg = f"Use `{ctx.prefix}set api timeseries api_key your_api_key_here`."
        await ctx.send(msg)

    @timeseriesset.command()
    async def detailed(self, ctx: commands.Context):
        """Toggles whether to send more detailed data (More resource intensive)."""
        state = await self.config_cache.get_set_detailed()
        await self.config_cache.get_set_detailed(set_to=not state)
        new_state = "Enabled" if not state else "Disabled"
        await ctx.send(f"Detailed stats submission: {new_state}")

    @timeseriesset.command()
    async def topggstats(self, ctx: commands.Context):
        """Toggles whether to send your Top.gg stats.
        
        For this you need a Top.gg token set like this `[p]set api dbl api_key keyhere`.
        """
        state = await self.config_cache.get_set_topgg()
        await self.config_cache.get_set_topgg(set_to=not state)
        new_state = "Enabled" if not state else "Disabled"
        await ctx.send(f"Top.gg stats submission: {new_state}")

    @timeseriesset.command()
    async def lightmode(self, ctx: commands.Context):
        """Toggle minimal data collection mode.

        Removes all joy and happiness from the cog, strip it from all the natural goodness and set it to operate in mininal mode.
        """
        state = await self.config_cache.get_set_lightmode()
        await self.config_cache.get_set_lightmode(set_to=not state)
        new_state = "Enabled" if not state else "Disabled"
        await ctx.send(f"Light mode (minimal data): {new_state}")
