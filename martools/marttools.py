from datetime import datetime, timezone

import apsw
import discord
import lavalink

from redbot.core import bank, commands
from redbot.core.data_manager import cog_data_path
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import bold, humanize_timedelta


try:
    from redbot.cogs.audio.audio_dataclasses import Query
except ImportError:
    Query = None

from .listeners import Listeners
from .statements import *
from .utils import rgetattr

_ = Translator("MartTools", __file__)


@cog_i18n(_)
class MartTools(Listeners, commands.Cog):
    """Multiple tools that are originally used on Martine the BOT."""

    __author__ = "Predä"
    __version__ = "1.5.0"

    def __init__(self, bot):
        self.bot = bot
        self._connection = apsw.Connection(str(cog_data_path(self) / "MartTools.db"))
        self.cursor = self._connection.cursor()
        self.cursor.execute(PRAGMA)
        self.cursor.execute(CREATE_TABLE_PERMA)
        self.cursor.execute(DROP_TEMP)
        self.cursor.execute(CREATE_TABLE_TEMP)
        self.uptime = datetime.now(tz=timezone.utc)

        if not Query:
            lavalink.register_event_listener(self.event_handler)  # To delete at next audio update.

    def upset(self, id: int, event: str):
        self.cursor.execute(UPSET_PERMA, (id, event))
        self.cursor.execute(UPSET_TEMP, (id, event))

    def fetch(self, key, id=None) -> int:
        if id is None:
            query = SELECT_PERMA_GLOBAL
            condition = {"event": key}
        else:
            query = SELECT_PERMA_SINGLE
            condition = {"event": key, "guild_id": id}
        result = self.cursor.execute(query, condition)
        return result[0] if result else 0

    def get(self, key, id=None) -> int:
        if id is None:
            query = SELECT_TEMP_GLOBAL
            condition = {"event": key}
        else:
            query = SELECT_TEMP_SINGLE
            condition = {"event": key, "guild_id": id}
        result = self.cursor.execute(query, condition)
        return result[0] if result else 0

    def cog_unload(self):  # To delete at next audio update.
        if not Query:
            lavalink.unregister_event_listener(self.event_handler)

    async def event_handler(self, player, event_type, extra):  # To delete at next audio update.
        if event_type == lavalink.LavalinkEvents.TRACK_START:
            self.upset(rgetattr(player, "channel.guild", 0), "tracks_played")

    def get_bot_uptime(self):
        delta = datetime.utcnow() - self.uptime
        uptime = humanize_timedelta(timedelta=delta)
        return uptime

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
                "Total accounts: **{all_accounts}**\nTotal amount: **{overall:,} {credits_name}**"
            ).format(all_accounts=all_accounts, overall=overall, credits_name=credits_name),
        )
        if pos is not None:
            percent = round((int(user_bal) / overall * 100), 3)
            em.add_field(
                name=_("Your stats:"),
                value=_(
                    "You have **{bal:,} {currency}**.\n"
                    "It's **{percent}%** of the {g}amount in the bank.\n"
                    "You are **{pos:,}/{all_accounts:,}** in the {g}leaderboard."
                ).format(
                    bal=user_bal,
                    currency=credits_name,
                    percent=percent,
                    g="global " if await bank.is_global() else "",
                    pos=pos,
                    all_accounts=all_accounts,
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
        commands_count = "`{:,}`".format(self.get("processed_commands"))
        errors_count = "`{:,}`".format(self.get("command_error"))
        messages_read = "`{:,}`".format(self.get("messages_read"))
        messages_sent = "`{:,}`".format(self.get("msg_sent"))
        try:
            total_num = "`{:,}/{:,}`".format(
                len(lavalink.active_players()), len(lavalink.all_players())
            )
        except AttributeError:
            total_num = "`{:,}/{:,}`".format(
                len([p for p in lavalink.players if p.current is not None]),
                len([p for p in lavalink.players]),
            )
        tracks_played = "`{:,}`".format(self.get("tracks_played"))
        guild_join = "`{:,}`".format(self.get("guild_join"))
        guild_leave = "`{:,}`".format(self.get("guild_remove"))
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

    @commands.command(aliases=["advusagec"])
    async def advusagecount(self, ctx):
        """
            Show the usage count of the bot.
            Commands processed, messages received, and music on servers.
        """
        uptime = str(self.get_bot_uptime())
        commands_count = "`{:,}`".format(self.fetch("processed_commands"))
        errors_count = "`{:,}`".format(self.fetch("command_error"))
        messages_read = "`{:,}`".format(self.fetch("messages_read"))
        messages_sent = "`{:,}`".format(self.fetch("msg_sent"))
        try:
            total_num = "`{:,}/{:,}`".format(
                len(lavalink.active_players()), len(lavalink.all_players())
            )
        except AttributeError:
            total_num = "`{:,}/{:,}`".format(
                len([p for p in lavalink.players if p.current is not None]),
                len([p for p in lavalink.players]),
            )
        tracks_played = "`{:,}`".format(self.fetch("tracks_played"))
        guild_join = "`{:,}`".format(self.fetch("guild_join"))
        guild_leave = "`{:,}`".format(self.fetch("guild_remove"))
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

    @commands.command(aliases=["prefixes"])
    async def prefix(self, ctx):
        """Show all prefixes of the bot"""
        default_prefixes = await ctx.bot.db.prefix()
        try:
            guild_prefixes = await ctx.bot.db.guild(ctx.guild).prefix()
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
        shards = self.bot.shard_count
        servers = len(self.bot.guilds)
        channels = sum(len(s.channels) for s in self.bot.guilds)
        total_users = sum(len(s.members) for s in self.bot.guilds)
        unique = len(self.bot.users)

        msg = _(
            "{name} is running on `{shards:,}` shard{s}.\n"
            "Serving `{servs:,}` servers (`{channels:,}` channels).\n"
            "For a total of `{users:,}` users (`{unique:,}` unique)."
        ).format(
            name=ctx.bot.user.name,
            shards=shards,
            s="s" if shards >= 2 else "",
            servs=servers,
            channels=channels,
            users=total_users,
            unique=unique,
        )
        try:
            em = discord.Embed(color=await ctx.embed_colour(), description=msg)
            await ctx.send(embed=em)
        except discord.Forbidden:
            await ctx.send(msg)

    @commands.command(aliases=["servreg"])
    async def serversregions(self, ctx):
        """Show total of regions where the bot is."""
        regions = {
            "vip-us-east": ":flag_us:" + _(" __VIP__ US East"),
            "vip-us-west": ":flag_us:" + _(" __VIP__ US West"),
            "vip-amsterdam": ":flag_nl:" + _(" __VIP__ Amsterdam"),
            "eu-west": ":flag_eu:" + _(" EU West"),
            "eu-central": ":flag_eu:" + _(" EU Central"),
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
        }
        region = {}
        for guild in self.bot.guilds:
            if str(guild.region):
                if str(guild.region) not in region:
                    region[str(guild.region)] = 0
                region[str(guild.region)] += 1
        divided = []
        for k, v in region.items():
            divided.append([k, v])
        divided = sorted(divided, key=lambda x: x[1], reverse=True)
        new = {}
        for entry in divided:
            new[entry[0]] = entry[1]
        msg = ""
        for k, v in new.items():
            msg += regions[str(k)] + f": `{v}`\n"
        guilds = len(self.bot.guilds)

        try:
            em = discord.Embed(
                color=await ctx.embed_colour(), title=_("Servers regions stats:"), description=msg
            )
            em.set_footer(text=_("For a total of {} servers").format(guilds))
            await ctx.send(embed=em)
        except discord.Forbidden:
            await ctx.send(
                bold(_("Servers regions stats:\n\n"))
                + msg
                + bold(_("\nFor a total of {} servers").format(guilds))
            )
