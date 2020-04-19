import discord

import lavalink

from redbot.core import bank, commands, checks
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import bold, humanize_timedelta
# from redbot.cogs.audio.localtracks import Query <- Will be probably changed

from datetime import datetime

_ = Translator("MartTools", __file__)


@cog_i18n(_)
class MartTools(commands.Cog):
    """Multiple tools that are originally used on Martine."""

    __author__ = "Predä"
    __version__ = "1.4.1"

    def __init__(self, bot):
        self.bot = bot
        lavalink.register_event_listener(self.event_handler)  # To delete at next audio update.

    def cog_unload(self):  # To delete at next audio update.
        lavalink.unregister_event_listener(self.event_handler)

    async def event_handler(self, player, event_type, extra):  # To delete at next audio update.
        # Thanks Draper#6666
        if event_type == lavalink.LavalinkEvents.TRACK_START:
            self.bot.counter["tracks_played"] += 1

    def get_bot_uptime(self):
        delta = datetime.utcnow() - self.bot.uptime
        uptime = humanize_timedelta(timedelta=delta)
        return uptime

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            self.bot.counter["command_error"] += 1

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            self.bot.counter["msg_sent"] += 1

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.bot.counter["guild_join"] += 1

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        self.bot.counter["guild_remove"] += 1

    # Planned for next audio update.
    # @commands.Cog.listener()
    # async def on_track_start(self, guild, track, requester):
    #     self.bot.counter["tracks_played"] += 1
    #     query = Query.process_input(track.uri)
    #     if track.is_stream:
    #         self.bot.counter["streams_played"] += 1
    #     if track.is_stream and query.is_youtube:
    #         self.bot.counter["yt_streams_played"] += 1
    #     if track.is_stream and query.is_mixer:
    #         self.bot.counter["mixer_streams_played"] += 1
    #     if track.is_stream and query.is_twitch:
    #         self.bot.counter["ttv_streams_played"] += 1
    #     if track.is_stream and query.is_other:
    #         self.bot.counter["other_streams_played"] += 1
    #     if query.is_youtube:
    #         self.bot.counter["youtube_tracks"] += 1
    #     if query.is_soundcloud:
    #         self.bot.counter["soundcloud_tracks"] += 1
    #     if query.is_bandcamp:
    #         self.bot.counter["bandcamp_tracks"] += 1
    #     if query.is_vimeo:
    #         self.bot.counter["vimeo_tracks"] += 1
    #     if query.is_mixer:
    #         self.bot.counter["mixer_tracks"] += 1
    #     if query.is_twitch:
    #         self.bot.counter["twitch_tracks"] += 1
    #     if query.is_other:
    #         self.bot.counter["other_tracks"] += 1

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
        if hasattr(bank, "_config"):
            bank_config = bank._config
        else:
            bank_config = bank._conf

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
        commands_count = "`{:,}`".format(self.bot.counter["processed_commands"])
        errors_count = "`{:,}`".format(self.bot.counter["command_error"])
        messages_read = "`{:,}`".format(self.bot.counter["messages_read"])
        messages_sent = "`{:,}`".format(self.bot.counter["msg_sent"])
        try:
            total_num = "`{:,}/{:,}`".format(
                len(lavalink.active_players()), len(lavalink.all_players())
            )
        except AttributeError:
            total_num = "`{:,}/{:,}`".format(
                len([p for p in lavalink.players if p.current is not None]),
                len([p for p in lavalink.players]),
            )
        tracks_played = "`{:,}`".format(self.bot.counter["tracks_played"])
        guild_join = "`{:,}`".format(self.bot.counter["guild_join"])
        guild_leave = "`{:,}`".format(self.bot.counter["guild_remove"])
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
