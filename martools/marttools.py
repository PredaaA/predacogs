import discord

import asyncio
import lavalink
import contextlib

from copy import copy
from datetime import datetime
from collections import Counter, defaultdict
from typing import Union  # <- Remove this at 3.2
from babel.numbers import format_decimal  # <- Remove this at 3.2

from redbot.core import Config, bank, commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import (
    bold,
    box,
    humanize_timedelta,
)  # , humanize_number <- Will be for 3.2

# from redbot.cogs.audio.dataclasses import Query

from .listeners import Listeners

_ = Translator("MartTools", __file__)


def humanize_number(val: Union[int, float]):  # <- Remove this at 3.2
    return format_decimal(val, locale="en_US")


@cog_i18n(_)
class MartTools(Listeners, commands.Cog):
    """Multiple tools that are originally used on Martine."""

    __author__ = "Predä"
    __version__ = "1.5.8"

    def __init__(self, bot):
        self.bot = bot
        self.counter = Counter()
        self.sticky_counter = Counter()
        self.config = Config.get_conf(self, 64481875498, force_registration=True)
        self._monitor_time = datetime.utcnow().timestamp()
        global_defauls = dict(
            command_error=0,
            msg_sent=0,
            dms_received=0,
            messages_read=0,
            guild_join=0,
            guild_remove=0,
            sessions_resumed=0,
            processed_commands=0,
            new_members=0,
            members_left=0,
            messages_deleted=0,
            messages_edited=0,
            reactions_added=0,
            reactions_removed=0,
            roles_added=0,
            roles_removed=0,
            roles_updated=0,
            members_banned=0,
            members_unbanned=0,
            emojis_removed=0,
            emojis_added=0,
            emojis_updated=0,
            users_joined_bot_music_room=0,
        )
        self.config.register_global(**global_defauls)
        self._task = self.bot.loop.create_task(self._save_counters_to_config())
        lavalink.register_event_listener(self.event_handler)  # To delete at next audio update.

    def cog_unload(self):
        lavalink.unregister_event_listener(self.event_handler)  # To delete at next audio update.
        self.bot.loop.create_task(self._clean_up())

    async def event_handler(self, player, event_type, extra):  # To delete at next audio update.
        # Thanks Draper#6666
        if event_type == lavalink.LavalinkEvents.TRACK_START:
            self.update_counters("tracks_played")

    def update_counters(self, key: str):
        self.counter[key] += 1
        self.sticky_counter[key] += 1

    def get_bot_uptime(self):
        delta = datetime.utcnow() - (
            self.bot.uptime if hasattr(self.bot, "uptime") else self.bot._uptime
        )
        uptime = humanize_timedelta(timedelta=delta)
        return uptime

    async def _save_counters_to_config(self):
        await self.bot.wait_until_ready()
        with contextlib.suppress(asyncio.CancelledError):
            while True:
                users_data = copy(self.sticky_counter)
                self.sticky_counter = Counter()
                async with self.config.all() as new_data:
                    for key, value in users_data.items():
                        if key in new_data:
                            new_data[key] += value
                        else:
                            new_data[key] = value
                    if "start_date" not in new_data:
                        new_data["start_date"] = self._monitor_time
                await asyncio.sleep(60)

    async def _clean_up(self):
        if self._task:
            self._task.cancel()
        async with self.config.all() as new_data:
            for key, value in self.sticky_counter.items():
                if key in new_data:
                    new_data[key] += value
                else:
                    new_data[key] = value

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    async def bankstats(self, ctx):
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
    async def usagecount(self, ctx):
        """
            Show the usage count of the bot.
            Commands processed, messages received, and music on servers.
        """
        uptime = str(self.get_bot_uptime())
        commands_count = "`{}`".format(humanize_number(self.counter["processed_commands"]))
        errors_count = "`{}`".format(humanize_number(self.counter["command_error"]))
        messages_read = "`{}`".format(humanize_number(self.counter["messages_read"]))
        messages_sent = "`{}`".format(humanize_number(self.counter["msg_sent"]))
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
        tracks_played = "`{}`".format(humanize_number(self.counter["tracks_played"]))
        guild_join = "`{}`".format(humanize_number(self.counter["guild_join"]))
        guild_leave = "`{}`".format(humanize_number(self.counter["guild_remove"]))
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
    async def advusagecount(self, ctx):
        """
        Same as [p]usagecount command but with more stats.
        """
        avatar = self.bot.user.avatar_url_as(static_format="png")
        counters = defaultdict(int, self.counter)
        uptime = str(self.get_bot_uptime())
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
            title=_("Usage count of {} since last restart:").format(ctx.bot.user.name),
            color=await ctx.embed_colour(),
        )
        em.add_field(
            name=_("Message Stats"),
            value=box(
                _(
                    "Messages Read       : {messages_read:,}\n"
                    "Messages Sent       : {msg_sent:,}\n"
                    "Messages Deleted    : {messages_deleted:,}\n"
                    "Messages Edited     : {messages_edited:,}\n"
                    "DMs Received        : {dms_received:,}\n"
                ).format_map(counters),
                lang="prolog",
            ),
            inline=False,
        )
        em.add_field(
            name=_("Commands Stats"),
            value=box(
                _(
                    "Commands Processed  : {processed_commands:,}\n"
                    "Errors Occured      : {command_error:,}\n"
                    "Sessions Resumed    : {sessions_resumed:,}\n"
                ).format_map(counters),
                lang="prolog",
            ),
            inline=False,
        )
        em.add_field(
            name=_("Guild Stats"),
            value=box(
                _(
                    "Guilds Joined       : {guild_join:,}\n"
                    "Guilds Left         : {guild_remove:,}\n"
                ).format_map(counters),
                lang="prolog",
            ),
            inline=False,
        )
        em.add_field(
            name=_("User Stats"),
            value=box(
                _(
                    "New Users           : {new_members:,}\n"
                    "Left Users          : {members_left:,}\n"
                    "Banned Users        : {members_banned:,}\n"
                    "Unbanned Users      : {members_unbanned:,}\n"
                ).format_map(counters),
                lang="prolog",
            ),
            inline=False,
        )
        em.add_field(
            name=_("Role Stats"),
            value=box(
                _(
                    "Roles Added         : {roles_added:,}\n"
                    "Roles Removed       : {roles_removed:,}\n"
                    "Roles Updated       : {roles_updated:,}\n"
                ).format_map(counters),
                lang="prolog",
            ),
            inline=False,
        )
        em.add_field(
            name=_("Emoji Stats"),
            value=box(
                _(
                    "Reacts Added        : {reactions_added:,}\n"
                    "Reacts Removed      : {reactions_removed:,}\n"
                    "Emoji Added         : {emojis_added:,}\n"
                    "Emoji Removed       : {emojis_removed:,}\n"
                    "Emoji Updated       : {emojis_updated:,}\n"
                ).format_map(counters),
                lang="prolog",
            ),
            inline=False,
        )
        em.add_field(
            name=_("Audio Stats"),
            value=box(
                _(
                    "Users Who Joined VC : {users_joined_bot_music_room:,}\n"
                    "Tracks Played       : {tracks_played:,}\n"
                    "Number Of Players   : {total_num}"
                ).format(
                    users_joined_bot_music_room=counters["users_joined_bot_music_room"],
                    tracks_played=counters["tracks_played"],
                    total_num=total_num,
                ),
                lang="prolog",
            ),
            inline=False,
        )
        em.set_thumbnail(url=avatar)
        em.set_footer(text=_("Since {}").format(uptime))
        await ctx.send(embed=em)

    @commands.command(aliases=["prefixes"])
    async def prefix(self, ctx):
        """Show all prefixes of the bot"""
        if hasattr(self.bot, "_config"):  # Red > 3.2
            default_prefixes = await self.bot._config.prefix()
            try:
                guild_prefixes = await self.bot._config.guild(ctx.guild).prefix()
            except AttributeError:
                guild_prefixes = False
        else:  # Red < 3.2
            default_prefixes = await self.bot.db.prefix()
            try:
                guild_prefixes = await self.bot.db.guild(ctx.guild).prefix()
            except AttributeError:
                guild_prefixes = False
        bot_name = ctx.bot.user.name
        avatar = self.bot.user.avatar_url_as(static_format="png")

        if not guild_prefixes:
            to_send = [f"`\u200b{p}\u200b`" for p in default_prefixes]
            plural = _("es") if len(default_prefixes) >= 2 else ""
            try:
                em = discord.Embed(color=await ctx.embed_colour())
                em.add_field(
                    name=_("Prefix{es} of {name}:").format(es=plural, name=bot_name),
                    value=" ".join(to_send),
                )
                em.set_thumbnail(url=avatar)
                await ctx.send(embed=em)
            except discord.Forbidden:
                await ctx.send(
                    bold(_("Prefix{es} of {name}:\n")).format(es=plural, name=bot_name)
                    + " ".join(to_send)
                )
        else:
            to_send = [f"`\u200b{p}\u200b`" for p in guild_prefixes]
            plural = _("es") if len(guild_prefixes) >= 2 else ""
            try:
                em = discord.Embed(color=await ctx.embed_colour())
                em.add_field(
                    name=_("Server prefix{es} of {name}:").format(es=plural, name=bot_name),
                    value=" ".join(to_send),
                )
                em.set_thumbnail(url=avatar)
                await ctx.send(embed=em)
            except discord.Forbidden:
                await ctx.send(
                    bold(_("Server prefix{es} of {name}:\n")).format(es=plural, name=bot_name)
                    + " ".join(to_send)
                )

    @commands.command(aliases=["serverc", "serversc"])
    async def servercount(self, ctx):
        """Send servers stats of the bot."""
        msg = _(
            "{name} is running on `{shards}` shard{s}.\n"
            "Serving `{servs}` servers (`{channels}` channels).\n"
            "For a total of `{users}` users (`{unique}` unique)."
        ).format(
            name=ctx.bot.user.name,
            shards=humanize_number(self.bot.shard_count),
            s="s" if self.bot.shard_count >= 2 else "",
            servs=humanize_number(len(self.bot.guilds)),
            channels=humanize_number(sum(len(s.channels) for s in self.bot.guilds)),
            users=humanize_number(sum(len(s.members) for s in self.bot.guilds)),
            unique=humanize_number(len(self.bot.users)),
        )
        try:
            em = discord.Embed(color=await ctx.embed_colour(), description=msg)
            await ctx.send(embed=em)
        except discord.Forbidden:
            await ctx.send(msg)

    @commands.command(aliases=["servreg"])
    async def serversregions(self, ctx, sort="guilds"):
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

        def sort_keys(key):
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
