import asyncio
import logging
import time
from collections import Counter
from datetime import datetime, timezone
from typing import Union

import discord
import lavalink
import sqlite3
from databases import Database
from redbot.cogs.audio.audio_dataclasses import Query
from redbot.core import bank, commands
from redbot.core.bot import Red
from redbot.core.cog_manager import cog_data_path
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import bold, box, humanize_number, humanize_timedelta

from .listeners import Listeners
from .statements import (
    CREATE_TABLE,
    CREATE_VERSION_TABLE,
    DROP_OLD_PERMA,
    DROP_OLD_TEMP,
    GET_EVENT_VALUE,
    INSERT_OR_IGNORE,
    SELECT_OLD,
    UPSERT,
    PRAGMA_journal_mode,
    PRAGMA_read_uncommitted,
    PRAGMA_wal_autocheckpoint,
)
from .utils import EVENTS_NAMES

log = logging.getLogger("red.predacogs.martools")
_ = Translator("MartTools", __file__)


@cog_i18n(_)
class MartTools(Listeners, commands.Cog):
    """Multiple tools that are originally used on Martine."""

    __author__ = ["Predä", "Draper"]
    __version__ = "3.0.2"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def __init__(self, bot: Red):
        self.bot = bot
        self.cursor = Database(f"sqlite:///{cog_data_path(self)}/MartTools.db")
        self.cache = {"perma": Counter(), "session": Counter()}
        self.uptime = discord.utils.utcnow()

        self.init_task = self.bot.loop.create_task(self.initialize())
        self.dump_cache_task = self.bot.loop.create_task(self._dump_cache_to_db_task())

    def cog_unload(self):
        self.dump_cache_task.cancel()
        if self.init_task:
            self.init_task.cancel()

        asyncio.create_task(self._dump_cache_to_db())

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    async def initialize(self):
        await self.cursor.connect()
        await self.cursor.execute(PRAGMA_journal_mode)
        await self.cursor.execute(PRAGMA_wal_autocheckpoint)
        await self.cursor.execute(PRAGMA_read_uncommitted)
        await self.cursor.execute(CREATE_TABLE)
        await self.cursor.execute(CREATE_VERSION_TABLE)
        await self.cursor.execute(
            INSERT_OR_IGNORE, {"event": "creation_time", "quantity": time.time()}
        )

        try:
            check_result = list(await self.cursor.fetch_all("SELECT * FROM bot_stats_perma"))
        except sqlite3.OperationalError:
            await self._populate_cache()
            return
        else:
            if check_result:
                await self._migrate_data()

        await self._populate_cache()

    async def _migrate_data(self):
        for event_name in EVENTS_NAMES:
            result = await self.cursor.fetch_val(SELECT_OLD, {"event": event_name})
            if result:
                await self.cursor.execute(UPSERT, {"event": event_name, "quantity": result})

        old_creation_time = await self.cursor.fetch_val(
            SELECT_OLD, {"event": "creation_time", "guild_id": -1000}
        )
        await self.cursor.execute(
            UPSERT,
            ("creation_time", old_creation_time or time.time()),
        )

        await self.cursor.execute(DROP_OLD_TEMP)
        await self.cursor.execute(DROP_OLD_PERMA)
        await self.cursor.execute("INSERT or IGNORE INTO version (version_num) VALUES (2)")

    async def _populate_cache(self):
        for event_name in EVENTS_NAMES:
            result = await self.cursor.fetch_val(GET_EVENT_VALUE, {"event": event_name})
            if result:
                self.cache["perma"][event_name] = result

        result = await self.cursor.fetch_val(GET_EVENT_VALUE, {"event": "creation_time"})
        self.cache["perma"]["creation_time"] = result or time.time()

    async def _dump_cache_to_db(self):
        for event_name, value in self.cache["perma"].items():
            await self.cursor.execute(UPSERT, {"event": event_name, "quantity": value})

    async def _dump_cache_to_db_task(self):
        await self.bot.wait_until_red_ready()
        while True:
            await asyncio.sleep(300)
            try:
                await self._dump_cache_to_db()
            except Exception:
                log.exception("Something went wrong in _dump_cache_to_db_task:")

    def get_value(self, key: str, perma: bool = False, raw: bool = False) -> Union[int, str]:
        if raw:
            return self.cache["perma" if perma else "session"][key]
        return humanize_number(self.cache["perma" if perma else "session"][key])

    def get_bot_uptime(self):
        delta = discord.utils.utcnow() - self.uptime
        return str(humanize_timedelta(timedelta=delta))

    def usage_counts_cpm(self, key: str, time: int = 60):
        delta = discord.utils.utcnow() - self.uptime
        minutes = delta.total_seconds() / time
        total = self.get_value(key, raw=True)
        return total / minutes

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    async def bankstats(self, ctx: commands.Context):
        """Show stats of the bank."""
        icon = self.bot.user.display_avatar
        user_bal = await bank.get_balance(ctx.author)
        credits_name = await bank.get_currency_name(ctx.guild)
        pos = await bank.get_leaderboard_position(ctx.author)
        bank_name = await bank.get_bank_name(ctx.guild)
        bank_config = bank._config

        if await bank.is_global():
            all_accounts = len(await bank_config.all_users())
            accounts = await bank_config.all_users()
        else:
            all_accounts = len(await bank_config.all_members(ctx.guild))
            accounts = await bank_config.all_members(ctx.guild)
        member_account = await bank.get_account(ctx.author)
        created_at = str(member_account.created_at)
        no = "1970-01-01 00:00:00"
        overall = 0
        for key, value in accounts.items():
            overall += value["balance"]

        em = discord.Embed(color=await ctx.embed_colour())
        em.set_author(name=_("{} stats:").format(bank_name), icon_url=icon)
        em.add_field(
            name=_("{} stats:").format("Global" if await bank.is_global() else "Bank"),
            value=_(
                "Total accounts: **{all_accounts}**\nTotal amount: **{overall} {credits_name}**"
            ).format(
                all_accounts=all_accounts,
                overall=humanize_number(overall),
                credits_name=credits_name,
            ),
        )
        if pos is not None:
            percent = round((int(user_bal) / overall * 100), 3)
            em.add_field(
                name=_("Your stats:"),
                value=_(
                    "You have **{bal} {currency}**.\n"
                    "It's **{percent}%** of the {g}amount in the bank.\n"
                    "You are **{pos}/{all_accounts}** in the {g}leaderboard."
                ).format(
                    bal=humanize_number(user_bal),
                    currency=credits_name,
                    percent=percent,
                    g="global " if await bank.is_global() else "",
                    pos=humanize_number(pos),
                    all_accounts=humanize_number(all_accounts),
                ),
                inline=False,
            )
        if created_at != no:
            em.set_footer(text=_("Bank account created on: ") + str(created_at))
        await ctx.send(embed=em)

    @commands.command(aliases=["usagec"])
    async def usagecount(self, ctx: commands.Context):
        """
        Show the usage count of the bot.
        Commands processed, messages received, and music on servers.
        """
        msg = _(
            "**Commands processed:** `{commands_count}` commands. (`{cpm_commands:.2f}`/min)\n"
            "**Commands errors:** `{errors_count}` errors.\n"
            "**Messages received:** `{messages_read}` messages. (`{cpm_msgs:.2f}`/min)\n"
            "**Messages sent:** `{messages_sent}` messages. (`{cpm_msgs_sent:.2f}`/min)\n"
            "**Playing music on:** `{ll_players}` servers.\n"
            "**Tracks played:** `{tracks_played}` tracks. (`{cpm_tracks:.2f}`/min)\n\n"
            "**Servers joined:** `{guild_join}` servers. (`{cpm_guild_join:.2f}`/hour)\n"
            "**Servers left:** `{guild_leave}` servers. (`{cpm_guild_leave:.2f}`/hour)"
        ).format(
            commands_count=self.get_value("processed_commands"),
            cpm_commands=self.usage_counts_cpm("processed_commands"),
            errors_count=self.get_value("command_error"),
            messages_read=self.get_value("messages_read"),
            cpm_msgs=self.usage_counts_cpm("messages_read"),
            messages_sent=self.get_value("msg_sent"),
            cpm_msgs_sent=self.usage_counts_cpm("msg_sent"),
            ll_players="`{}/{}`".format(
                humanize_number(len(lavalink.active_players())),
                humanize_number(len(lavalink.all_players())),
            ),
            tracks_played=self.get_value("tracks_played"),
            cpm_tracks=self.usage_counts_cpm("tracks_played"),
            guild_join=self.get_value("guild_join"),
            cpm_guild_join=self.usage_counts_cpm("guild_join", 3600),
            guild_leave=self.get_value("guild_remove"),
            cpm_guild_leave=self.usage_counts_cpm("guild_remove", 3600),
        )
        if await ctx.embed_requested():
            em = discord.Embed(
                color=await ctx.embed_colour(),
                title=_("Usage count of {} since last restart:").format(self.bot.user.name),
                description=msg,
            )
            em.set_thumbnail(url=self.bot.user.display_avatar)
            em.set_footer(text=_("Since {}").format(self.get_bot_uptime()))
            await ctx.send(embed=em)
        else:
            await ctx.send(
                _("Usage count of {} since last restart:\n").format(ctx.bot.user.name)
                + msg
                + _("\n\nSince {}").format(self.get_bot_uptime())
            )

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["advusagec"])
    async def advusagecount(self, ctx: commands.Context):
        """
        Permanent stats since first time that the cog has been loaded.
        """
        avatar = self.bot.user.display_avatar
        delta = discord.utils.utcnow() - datetime.fromtimestamp(
            self.get_value("creation_time", perma=True, raw=True), timezone.utc
        )
        uptime = humanize_timedelta(timedelta=delta)
        ll_players = "{}/{}".format(
            humanize_number(len(lavalink.active_players())),
            humanize_number(len(lavalink.all_players())),
        )

        em = discord.Embed(
            title=_("Usage count of {}:").format(ctx.bot.user.name),
            color=await ctx.embed_colour(),
        )
        em.add_field(
            name=_("Message Stats"),
            value=box(
                _(
                    "Messages Read       : {messages_read}\n"
                    "Messages Sent       : {msg_sent}\n"
                    "Messages Deleted    : {messages_deleted}\n"
                    "Messages Edited     : {messages_edited}\n"
                    "DMs Received        : {dms_received}\n"
                ).format_map(
                    {
                        "messages_read": self.get_value("messages_read", perma=True),
                        "msg_sent": self.get_value("msg_sent", perma=True),
                        "messages_deleted": self.get_value("messages_deleted", perma=True),
                        "messages_edited": self.get_value("messages_edited", perma=True),
                        "dms_received": self.get_value("dms_received", perma=True),
                    }
                ),
                lang="prolog",
            ),
            inline=False,
        )
        em.add_field(
            name=_("Commands Stats"),
            value=box(
                _(
                    "Commands Processed  : {processed_commands}\n"
                    "Errors Occured      : {command_error}\n"
                    "Sessions Resumed    : {sessions_resumed}\n"
                ).format_map(
                    {
                        "processed_commands": self.get_value("processed_commands", perma=True),
                        "command_error": self.get_value("command_error", perma=True),
                        "sessions_resumed": self.get_value("sessions_resumed", perma=True),
                    }
                ),
                lang="prolog",
            ),
            inline=False,
        )
        em.add_field(
            name=_("Guild Stats"),
            value=box(
                _(
                    "Guilds Joined       : {guild_join}\n" "Guilds Left         : {guild_remove}\n"
                ).format_map(
                    {
                        "guild_join": self.get_value("guild_join", perma=True),
                        "guild_remove": self.get_value("guild_remove", perma=True),
                    }
                ),
                lang="prolog",
            ),
            inline=False,
        )
        em.add_field(
            name=_("User Stats"),
            value=box(
                _(
                    "New Users           : {new_members}\n"
                    "Left Users          : {members_left}\n"
                    "Banned Users        : {members_banned}\n"
                    "Unbanned Users      : {members_unbanned}\n"
                ).format_map(
                    {
                        "new_members": self.get_value("new_members", perma=True),
                        "members_left": self.get_value("members_left", perma=True),
                        "members_banned": self.get_value("members_banned", perma=True),
                        "members_unbanned": self.get_value("members_unbanned", perma=True),
                    }
                ),
                lang="prolog",
            ),
            inline=False,
        )
        em.add_field(
            name=_("Role Stats"),
            value=box(
                _(
                    "Roles Added         : {roles_added}\n"
                    "Roles Removed       : {roles_removed}\n"
                    "Roles Updated       : {roles_updated}\n"
                ).format_map(
                    {
                        "roles_added": self.get_value("roles_added", perma=True),
                        "roles_removed": self.get_value("roles_removed", perma=True),
                        "roles_updated": self.get_value("roles_updated", perma=True),
                    }
                ),
                lang="prolog",
            ),
            inline=False,
        )
        em.add_field(
            name=_("Emoji Stats"),
            value=box(
                _(
                    "Reacts Added        : {reactions_added}\n"
                    "Reacts Removed      : {reactions_removed}\n"
                    "Emoji Added         : {emojis_added}\n"
                    "Emoji Removed       : {emojis_removed}\n"
                    "Emoji Updated       : {emojis_updated}\n"
                ).format_map(
                    {
                        "reactions_added": self.get_value("reactions_added", perma=True),
                        "reactions_removed": self.get_value("reactions_removed", perma=True),
                        "emojis_added": self.get_value("emojis_added", perma=True),
                        "emojis_removed": self.get_value("emojis_removed", perma=True),
                        "emojis_updated": self.get_value("emojis_updated", perma=True),
                    }
                ),
                lang="prolog",
            ),
            inline=False,
        )
        em.add_field(
            name=_("Audio Stats"),
            value=box(
                _(
                    "Users Who Joined VC : {users_joined_bot_music_room}\n"
                    "Tracks Played       : {tracks_played}\n"
                    "Number Of Players   : {ll_players}"
                ).format(
                    users_joined_bot_music_room=self.get_value(
                        "users_joined_bot_music_room", perma=True
                    ),
                    tracks_played=self.get_value("tracks_played", perma=True),
                    ll_players=ll_players,
                ),
                lang="prolog",
            ),
            inline=False,
        )
        if Query:
            em.add_field(
                name=_("Track Stats"),
                value=box(
                    _(
                        "Streams             : {streams_played}\n"
                        "YouTube Streams     : {yt_streams_played}\n"
                        "Twitch Streams      : {ttv_streams_played}\n"
                        "Other Streams       : {streams_played}\n"
                        "YouTube Tracks      : {youtube_tracks}\n"
                        "Soundcloud Tracks   : {soundcloud_tracks}\n"
                        "Bandcamp Tracks     : {bandcamp_tracks}\n"
                        "Vimeo Tracks        : {vimeo_tracks}\n"
                        "Twitch Tracks       : {twitch_tracks}\n"
                        "Other Tracks        : {other_tracks}\n"
                    ).format(
                        streams_played=self.get_value("streams_played", perma=True),
                        yt_streams_played=self.get_value("yt_streams_played", perma=True),
                        ttv_streams_played=self.get_value("ttv_streams_played", perma=True),
                        other_streams_played=self.get_value("other_streams_played", perma=True),
                        youtube_tracks=self.get_value("youtube_tracks", perma=True),
                        soundcloud_tracks=self.get_value("soundcloud_tracks", perma=True),
                        bandcamp_tracks=self.get_value("bandcamp_tracks", perma=True),
                        vimeo_tracks=self.get_value("vimeo_tracks", perma=True),
                        twitch_tracks=self.get_value("twitch_tracks", perma=True),
                        other_tracks=self.get_value("other_tracks", perma=True),
                    ),
                    lang="prolog",
                ),
                inline=False,
            )

        em.set_thumbnail(url=avatar)
        em.set_footer(text=_("Since {}").format(uptime))
        await ctx.send(embed=em)

    @commands.command(aliases=["prefixes"])
    async def prefix(self, ctx: commands.Context):
        """Show all prefixes of the bot"""
        default_prefixes = await self.bot._config.prefix()
        try:
            guild_prefixes = await self.bot._config.guild(ctx.guild).prefix()
        except AttributeError:
            guild_prefixes = False
        bot_name = ctx.bot.user.name
        avatar = self.bot.user.display_avatar

        if not guild_prefixes:
            to_send = [f"`\u200b{p}\u200b`" for p in default_prefixes]
            plural = _("Prefixes") if len(default_prefixes) >= 2 else _("Prefix")
            if await ctx.embed_requested():
                em = discord.Embed(
                    color=await ctx.embed_colour(),
                    title=_("{} of {}:").format(plural, bot_name),
                    description=" ".join(to_send),
                )
                em.set_thumbnail(url=avatar)
                await ctx.send(embed=em)
            else:
                await ctx.send(bold(_("{} of {}:\n")).format(plural, bot_name) + " ".join(to_send))
        else:
            to_send = [f"`\u200b{p}\u200b`" for p in guild_prefixes]
            plural = _("prefixes") if len(default_prefixes) >= 2 else _("prefix")
            if await ctx.embed_requested():
                em = discord.Embed(
                    color=await ctx.embed_colour(),
                    title=_("Server {} of {}:").format(plural, bot_name),
                    description=" ".join(to_send),
                )
                em.set_thumbnail(url=avatar)
                await ctx.send(embed=em)
            else:
                await ctx.send(
                    bold(_("Server {} of {name}:\n")).format(plural, bot_name) + " ".join(to_send)
                )

    @commands.command(aliases=["serverc", "serversc"])
    async def servercount(self, ctx: commands.Context):
        """Send servers stats of the bot."""
        visible_users = sum(len(s.members) for s in self.bot.guilds)
        total_users = sum(s.member_count for s in self.bot.guilds)
        msg = _(
            "{name} is running on `{shard_count}` {shards}.\n"
            "Serving `{servs}` servers (`{channels}` channels).\n"
            "For a total of `{visible_users}` users (`{unique}` unique).\n"
            "(`{visible_users}` visible now, `{total_users}` total, `{percentage_chunked:.2f}%` chunked)"
        ).format(
            name=ctx.bot.user.name,
            shard_count=humanize_number(self.bot.shard_count),
            shards=_("shards") if self.bot.shard_count > 1 else _("shard"),
            servs=humanize_number(len(self.bot.guilds)),
            channels=humanize_number(sum(len(s.channels) for s in self.bot.guilds)),
            visible_users=humanize_number(visible_users),
            unique=humanize_number(len(self.bot.users)),
            total_users=humanize_number(total_users),
            percentage_chunked=visible_users / total_users * 100,
        )
        if await ctx.embed_requested():
            em = discord.Embed(color=await ctx.embed_colour(), description=msg)
            await ctx.send(embed=em)
        else:
            await ctx.send(msg)

    @commands.command(aliases=["servreg"])
    async def serversregions(self, ctx: commands.Context, sort: str = "guilds"):
        """
        Show total of regions where the bot is.

        You can also sort by number of users by using `[p]serversregions users`
        By default it sort by guilds.
        """
        regions_dict = {
            "vip-us-east": ":flag_us:" + _(" __VIP__ US East"),
            "vip-us-west": ":flag_us:" + _(" __VIP__ US West"),
            "vip-amsterdam": ":flag_nl:" + _(" __VIP__ Amsterdam"),
            "eu-west": ":flag_eu:" + _(" EU West"),
            "eu-central": ":flag_eu:" + _(" EU Central"),
            "europe": ":flag_eu:" + _(" Europe"),
            "london": ":flag_gb:" + _(" London"),
            "frankfurt": ":flag_de:" + _(" Frankfurt"),
            "amsterdam": ":flag_nl:" + _(" Amsterdam"),
            "us-west": ":flag_us:" + _(" US West"),
            "us-east": ":flag_us:" + _(" US East"),
            "us-south": ":flag_us:" + _(" US South"),
            "us-central": ":flag_us:" + _(" US Central"),
            "singapore": ":flag_sg:" + _(" Singapore"),
            "sydney": ":flag_au:" + _(" Sydney"),
            "brazil": ":flag_br:" + _(" Brazil"),
            "hongkong": ":flag_hk:" + _(" Hong Kong"),
            "russia": ":flag_ru:" + _(" Russia"),
            "japan": ":flag_jp:" + _(" Japan"),
            "southafrica": ":flag_za:" + _(" South Africa"),
            "india": ":flag_in:" + _(" India"),
            "dubai": ":flag_ae:" + _(" Dubai"),
            "south-korea": ":flag_kr:" + _(" South Korea"),
            "newark": ":flag_us:" + _(" Newark"),
            "atlanta": ":flag_us:" + _(" Atlanta"),
            "santa-clara": ":flag_us:" + _(" Santa Clara"),
            "seattle": ":flag_us:" + _(" Seattle"),
            "st-pete": ":flag_us:" + _(" St. Petersburg"),
            "buenos-aires": ":flag_ar:" + _(" Buenos Aires"),
            "stockholm": ":flag_se: " + _(" Stockholm"),
            "santiago": ":flag_cl: " + _(" Santiago"),
        }
        regions = {}
        for guild in self.bot.guilds:
            region = str(guild.region)
            if region not in regions:
                regions[region] = {"guilds": 0, "users": 0}
            regions[region]["users"] += guild.member_count
            regions[region]["guilds"] += 1

        def sort_keys(key: str):
            keys = (
                (key[1]["guilds"], key[1]["users"])
                if sort != "users"
                else (key[1]["users"], key[1]["guilds"])
            )
            return keys

        regions_stats = dict(sorted(regions.items(), key=lambda x: sort_keys(x), reverse=True))

        msg = [
            _("{flag}: {guilds_len} and {users_len}").format(
                flag=regions_dict.get(region_name, region_name),
                guilds_len=(
                    f"`{humanize_number(values['guilds'])} {_('server') if values['guilds'] < 2 else _('servers')}`"
                ),
                users_len=(
                    f"`{humanize_number(values['users'])} {_('user') if values['users'] < 2 else _('users')}`"
                ),
            )
            for region_name, values in regions_stats.items()
        ]
        guilds_word = _("server") if len(self.bot.guilds) < 2 else _("servers")
        users_word = (
            _("user") if sum(k["users"] for k in regions_stats.values()) < 2 else _("users")
        )
        footer = _("For a total of {guilds} and {users}").format(
            guilds=f"{humanize_number(len(self.bot.guilds))} {guilds_word}",
            users=f"{humanize_number(sum(k['users'] for k in regions_stats.values()))} {users_word}",
        )

        if await ctx.embed_requested():
            em = discord.Embed(
                color=await ctx.embed_colour(),
                title=_("Servers regions stats:"),
                description="\n".join(msg),
            )
            em.set_footer(text=footer)
            await ctx.send(embed=em)
        else:
            msg = bold(_("Servers regions stats:\n\n")) + "\n".join(msg) + "\n" + bold(footer)
            await ctx.send(msg)
