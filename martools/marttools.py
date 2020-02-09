import contextlib
import time
from collections import Counter, defaultdict
from copy import copy
from datetime import datetime

import discord
import lavalink
from redbot.core import Config, bank, commands
from redbot.core.bot import Red
from redbot.core.data_manager import cog_data_path
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import (bold, box, humanize_number,
                                               humanize_timedelta)

import apsw

from .listeners import Listeners
from .statements import *
from .utils import rgetattr

try:
    from redbot.cogs.audio.audio_dataclasses import Query
except ImportError:
    Query = None




_ = Translator("MartTools", __file__)


@cog_i18n(_)
class MartTools(Listeners, commands.Cog):
    """Multiple tools that are originally used on Martine."""

    __author__ = "Predä"
    __version__ = "1.7"

    def __init__(self, bot: Red):
        self.bot = bot
        self._connection = apsw.Connection(str(cog_data_path(self) / "MartTools.db"))
        self.cursor = self._connection.cursor()
        self.cursor.execute(PRAGMA_journal_mode)
        self.cursor.execute(PRAGMA_wal_autocheckpoint)
        self.cursor.execute(PRAGMA_read_uncommitted)
        self.cursor.execute(CREATE_TABLE_PERMA)
        self.cursor.execute(DROP_TEMP)
        self.cursor.execute(CREATE_TABLE_TEMP)
        self.uptime = datetime.utcnow()
        self.cursor.execute(INSERT_PERMA_DO_NOTHING, (-1000, "creation_time", time.time()))

    def upsert(self, id: int, event: str):
        self.cursor.execute(UPSERT_PERMA, (id, event))
        self.cursor.execute(UPSERT_TEMP, (id, event))

    def fetch(self, key, id=None) -> str:
        if id is None:
            query = SELECT_PERMA_GLOBAL
            condition = {"event": key}
        else:
            query = SELECT_PERMA_SINGLE
            condition = {"event": key, "guild_id": id}
        result = list(self.cursor.execute(query, condition))
        return humanize_number(result[0][0] if result else 0)

    def get(self, key, id=None) -> str:
        if id is None:
            query = SELECT_TEMP_GLOBAL
            condition = {"event": key}
        else:
            query = SELECT_TEMP_SINGLE
            condition = {"event": key, "guild_id": id}
        result = list(self.cursor.execute(query, condition))
        return humanize_number(result[0][0] if result else 0)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"

    def cog_unload(self):
        self._connection.close()

    def get_bot_uptime(self):
        delta = datetime.utcnow() - self.uptime
        uptime = humanize_timedelta(timedelta=delta)
        return uptime

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    async def bankstats(self, ctx: commands.Context):
        """Show stats of the bank."""
        icon = self.bot.user.avatar_url_as(static_format="png")
        user_bal = await bank.get_balance(ctx.author)
        credits_name = await bank.get_currency_name(ctx.guild)
        pos = await bank.get_leaderboard_position(ctx.author)
        bank_name = await bank.get_bank_name(ctx.guild)
        if await bank.is_global():
            all_accounts = len(await bank._conf.all_users())
            accounts = await bank._conf.all_users()
        else:
            all_accounts = len(await bank._conf.all_members(ctx.guild))
            accounts = await bank._conf.all_members(ctx.guild)
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
        uptime = str(self.get_bot_uptime())
        commands_count = "`{}`".format(self.get("processed_commands"))
        errors_count = "`{}`".format(self.get("command_error"))
        messages_read = "`{}`".format(self.get("messages_read"))
        messages_sent = "`{}`".format(self.get("msg_sent"))
        try:
            total_num = "`{}/{}`".format(
                humanize_number(len(lavalink.active_players())),
                humanize_number(len(lavalink.all_players())),
            )
        except AttributeError:  # Remove at 3.2
            total_num = "`{}/{}`".format(
                humanize_number(len([p for p in lavalink.players if p.current is not None])),
                humanize_number(len([p for p in lavalink.players])),
            )
        tracks_played = "`{}`".format(self.get("tracks_played"))
        guild_join = "`{}`".format(self.get("guild_join"))
        guild_leave = "`{}`".format(self.get("guild_remove"))
        avatar = self.bot.user.avatar_url_as(static_format="png")
        msg = (
            bold(_("Commands processed: "))
            + _("{} commands.\n").format(commands_count)
            + bold(_("Commands errors: "))
            + _("{} errors.\n").format(errors_count)
            + bold(_("Messages received: "))
            + _("{} messages.\n").format(messages_read)
            + bold(_("Messages sent: "))
            + _("{} messages.\n").format(messages_sent)
            + bold(_("Playing music on: "))
            + _("{} servers.\n").format(total_num)
            + bold(_("Tracks played: "))
            + _("{} tracks.\n\n").format(tracks_played)
            + bold(_("Servers joined: "))
            + _("{} servers.\n").format(guild_join)
            + bold(_("Servers left: "))
            + _("{} servers.").format(guild_leave)
        )
        try:
            em = discord.Embed(color=await ctx.embed_colour())
            em.add_field(
                name=_("Usage count of {} since last restart:").format(ctx.bot.user.name),
                value=msg,
            )
            em.set_thumbnail(url=avatar)
            em.set_footer(text=_("Since {}").format(uptime))
            await ctx.send(embed=em)
        except discord.Forbidden:
            await ctx.send(
                _("Usage count of {} since last restart:\n").format(ctx.bot.user.name)
                + msg
                + _("\n\nSince {}").format(uptime)
            )

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["advusagec"])
    async def advusagecount(self, ctx: commands.Context):
        """
        Same as [p]usagecount command but with more stats.
        """
        avatar = self.bot.user.avatar_url_as(static_format="png")
        query = SELECT_PERMA_SINGLE
        condition = {"event": "creation_time", "guild_id": -1000}
        result = list(self.cursor.execute(query, condition))
        delta = datetime.utcnow() - datetime.utcfromtimestamp(result[0][0])
        uptime = humanize_timedelta(timedelta=delta)
        try:
            total_num = "{}/{}".format(
                humanize_number(len(lavalink.active_players())),
                humanize_number(len(lavalink.all_players())),
            )
        except AttributeError:  # Remove at 3.2
            total_num = "{}/{}".format(
                humanize_number(len([p for p in lavalink.players if p.current is not None])),
                humanize_number(len([p for p in lavalink.players])),
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
                        "messages_read": self.fetch("messages_read"),
                        "msg_sent": self.fetch("msg_sent"),
                        "messages_deleted": self.fetch("messages_deleted"),
                        "messages_edited": self.fetch("messages_edited"),
                        "dms_received": self.fetch("dms_received"),
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
                        "processed_commands": self.fetch("processed_commands"),
                        "command_error": self.fetch("command_error"),
                        "sessions_resumed": self.fetch("sessions_resumed"),
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
                        "guild_join": self.fetch("guild_join"),
                        "guild_remove": self.fetch("guild_remove"),
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
                        "new_members": self.fetch("new_members"),
                        "members_left": self.fetch("members_left"),
                        "members_banned": self.fetch("members_banned"),
                        "members_unbanned": self.fetch("members_unbanned"),
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
                        "roles_added": self.fetch("roles_added"),
                        "roles_removed": self.fetch("roles_removed"),
                        "roles_updated": self.fetch("roles_updated"),
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
                        "reactions_added": self.fetch("reactions_added"),
                        "reactions_removed": self.fetch("reactions_removed"),
                        "emojis_added": self.fetch("emojis_added"),
                        "emojis_removed": self.fetch("emojis_removed"),
                        "emojis_updated": self.fetch("emojis_updated"),
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
                    "Number Of Players   : {total_num}"
                ).format(
                    users_joined_bot_music_room=self.fetch("users_joined_bot_music_room"),
                    tracks_played=self.fetch("tracks_played"),
                    total_num=total_num,
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
                        "Mixer Streams       : {mixer_streams_played}\n"
                        "Twitch Streams      : {ttv_streams_played}\n"
                        "Other Streams       : {streams_played}\n"
                        "YouTube Tracks      : {youtube_tracks}\n"
                        "Soundcloud Tracks   : {soundcloud_tracks}\n"
                        "Bandcamp Tracks     : {bandcamp_tracks}\n"
                        "Vimeo Tracks        : {vimeo_tracks}\n"
                        "Mixer Tracks        : {mixer_tracks}\n"
                        "Twitch Tracks       : {twitch_tracks}\n"
                        "Other Tracks        : {other_tracks}\n"
                    ).format(
                        streams_played=self.fetch("streams_played"),
                        yt_streams_played=self.fetch("yt_streams_played"),
                        mixer_streams_played=self.fetch("mixer_streams_played"),
                        ttv_streams_played=self.fetch("ttv_streams_played"),
                        other_streams_played=self.fetch("other_streams_played"),
                        youtube_tracks=self.fetch("youtube_tracks"),
                        soundcloud_tracks=self.fetch("soundcloud_tracks"),
                        bandcamp_tracks=self.fetch("bandcamp_tracks"),
                        vimeo_tracks=self.fetch("vimeo_tracks"),
                        mixer_tracks=self.fetch("mixer_tracks"),
                        twitch_tracks=self.fetch("twitch_tracks"),
                        other_tracks=self.fetch("other_tracks"),
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
        avatar = self.bot.user.avatar_url_as(static_format="png")

        if not guild_prefixes:
            to_send = [f"`\u200b{p}\u200b`" for p in default_prefixes]
            plural = _("Prefixes") if len(default_prefixes) >= 2 else _("Prefix")
            try:
                em = discord.Embed(
                    color=await ctx.embed_colour(),
                    title=_("{} of {}:").format(plural, bot_name),
                    description=" ".join(to_send),
                )
                em.set_thumbnail(url=avatar)
                await ctx.send(embed=em)
            except discord.Forbidden:
                await ctx.send(bold(_("{} of {}:\n")).format(plural, bot_name) + " ".join(to_send))
        else:
            to_send = [f"`\u200b{p}\u200b`" for p in guild_prefixes]
            plural = _("prefixes") if len(default_prefixes) >= 2 else _("prefix")
            try:
                em = discord.Embed(
                    color=await ctx.embed_colour(),
                    title=_("Server {} of {}:").format(plural, bot_name),
                    description=" ".join(to_send),
                )
                em.set_thumbnail(url=avatar)
                await ctx.send(embed=em)
            except discord.Forbidden:
                await ctx.send(
                    bold(_("Server {} of {name}:\n")).format(plural, bot_name) + " ".join(to_send)
                )

    @commands.command(aliases=["serverc", "serversc"])
    async def servercount(self, ctx: commands.Context):
        """Send servers stats of the bot."""
        msg = _(
            "{name} is running on `{shard_count}` {shards}.\n"
            "Serving `{servs}` servers (`{channels}` channels).\n"
            "For a total of `{users}` users (`{unique}` unique).\n"
            "(`{users}` visible now, `{real_total}` total)"
        ).format(
            name=ctx.bot.user.name,
            shard_count=humanize_number(self.bot.shard_count),
            shards=_("shards") if self.bot.shard_count > 1 else _("shard"),
            servs=humanize_number(len(self.bot.guilds)),
            channels=humanize_number(sum(len(s.channels) for s in self.bot.guilds)),
            users=humanize_number(sum(len(s.members) for s in self.bot.guilds)),
            unique=humanize_number(len(self.bot.users)),
            real_total=humanize_number(sum(s.member_count for s in self.bot.guilds)),
        )
        try:
            em = discord.Embed(color=await ctx.embed_colour(), description=msg)
            await ctx.send(embed=em)
        except discord.Forbidden:
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
                flag=regions_dict[region_name],
                guilds_len=(
                    f"`{values['guilds']:,} {_('server') if values['guilds'] < 2 else _('servers')}`"
                ),
                users_len=(
                    f"`{values['users']:,} {_('user') if values['users'] < 2 else _('users')}`"
                ),
            )
            for region_name, values in regions_stats.items()
        ]
        guilds_word = _("server") if len(self.bot.guilds) < 2 else _("servers")
        users_word = (
            _("user") if sum(k["users"] for k in regions_stats.values()) < 2 else _("users")
        )
        footer = _("For a total of {guilds} and {users}").format(
            guilds=f"{len(self.bot.guilds):,} {guilds_word}",
            users=f"{sum(k['users'] for k in regions_stats.values()):,} {users_word}",
        )

        try:
            em = discord.Embed(
                color=await ctx.embed_colour(),
                title=_("Servers regions stats:"),
                description="\n".join(msg),
            )
            em.set_footer(text=footer)
            await ctx.send(embed=em)
        except discord.Forbidden:
            msg = bold(_("Servers regions stats:\n\n")) + "\n".join(msg) + "\n" + bold(footer)
            await ctx.send(msg)
