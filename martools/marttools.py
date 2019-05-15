import discord

from redbot.core import bank, commands, checks
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import bold

import lavalink

_ = Translator("MartTools", __file__)


@cog_i18n(_)
class MartTools(commands.Cog):
    """Multiple tools that are originally used on Martine the BOT."""

    __author__ = "Predä"
    __version__ = "1.1.0"

    def __init__(self, bot):
        self.bot = bot

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

    @commands.command()
    @commands.guild_only()
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
            em.set_footer(text=_("Account created on: ") + str(created_at))
        await ctx.send(embed=em)

    @commands.command(aliases=["usagec"])
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def usagecount(self, ctx):
        """
            Show the usage count of the bot.
            Commands processed, messages received, and music on servers.
        """
        uptime = str(self.bot.get_cog("Core").get_bot_uptime())
        commands_count = "`{:,}`".format(self.bot.counter["processed_commands"])
        errors_count = "`{}`".format(self.bot.counter["command_error"])
        messages_read = "`{:,}`".format(self.bot.counter["messages_read"])
        messages_sent = "`{:,}`".format(self.bot.counter["msg_sent"])
        try:
            total_num = "`{:,}/{:,}`".format(
                len(lavalink.active_players()), len(lavalink.all_players())
            )
        except AttributeError:
            total_num = "`{:,}/{:,}`".format(
                len([p for p in lavalink.players if p.current is None]),
                len([p for p in lavalink.players if p.current is not None]),
            )
        guild_join = "`{:,}`".format(self.bot.counter["guild_join"])
        guild_leave = "`{:,}`".format(self.bot.counter["guild_remove"])
        avatar = self.bot.user.avatar_url_as(static_format="png")

        em = discord.Embed(color=(await ctx.embed_colour()))
        em.add_field(
            name=_("Usage count of {} since last restart:").format(ctx.bot.user.name),
            value=(
                bold(_("Commands processed: "))
                + _("{} commands.\n").format(commands_count)
                + bold(_("Commands errors:"))
                + _(" {} errors.\n").format(errors_count)
                + bold(_("Messages received:"))
                + _(" {} messages.\n").format(messages_read)
                + bold(_("Messages sent:"))
                + _(" {} messages.\n").format(messages_sent)
                + bold(_("Playing music on:"))
                + _(" {} servers.\n\n").format(total_num)
                + bold(_("Servers joined:"))
                + _(" {} servers.\n").format(guild_join)
                + bold(_("Servers left:"))
                + _(" {} servers.").format(guild_leave)
            ),
        )
        em.set_thumbnail(url=avatar)
        em.set_footer(text=_("Since {}").format(uptime))
        await ctx.send(embed=em)

    @commands.command(aliases=["prefixes"])
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def prefix(self, ctx):
        """Show all prefixes of the bot"""
        default_prefixes = await ctx.bot.db.prefix()
        guild_prefixes = await ctx.bot.db.guild(ctx.guild).prefix()
        bot_name = ctx.bot.user.name
        avatar = self.bot.user.avatar_url_as(static_format="png")

        if not guild_prefixes:
            to_send = [f"`\u200b{p}\u200b`" for p in default_prefixes]
            prefix_string = " ".join(to_send)
            em = discord.Embed(color=(await ctx.embed_colour()))
            em.add_field(
                name=_("Prefix{es} of {name}:").format(
                    es="es" if len(default_prefixes) >= 2 else "", name=bot_name
                ),
                value=prefix_string,
            )
            em.set_thumbnail(url=avatar)
            await ctx.send(embed=em)
        else:
            to_send = [f"`\u200b{p}\u200b`" for p in guild_prefixes]
            prefix_string = " ".join(to_send)
            em = discord.Embed(color=(await ctx.embed_colour()))
            em.add_field(
                name=_("Server prefix{es} of {name}:").format(
                    es="es" if len(guild_prefixes) >= 2 else "", name=bot_name
                ),
                value=prefix_string,
            )
            em.set_thumbnail(url=avatar)
            await ctx.send(embed=em)

    @commands.command(aliases=["serverc", "serversc"])
    @commands.bot_has_permissions(embed_links=True)
    async def servercount(self, ctx):
        """Send servers stats of the bot."""
        shards = self.bot.shard_count
        servers = len(self.bot.guilds)
        channels = sum(len(s.channels) for s in self.bot.guilds)
        total_users = sum(len(s.members) for s in self.bot.guilds)
        unique = len(self.bot.users)

        em = discord.Embed(
            color=(await ctx.embed_colour()),
            description=_(
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
            ),
        )
        await ctx.send(embed=em)

    @commands.command(aliases=["servreg"])
    @commands.guild_only()
    async def serversregions(self, ctx):
        """Show total of regions where the bot is."""
        regions = {
            "vip-us-east": _("__VIP__ US East") + " :flag_us:",
            "vip-us-west": _("__VIP__ US West") + " :flag_us:",
            "vip-amsterdam": _("__VIP__ Amsterdam") + " :flag_nl:",
            "eu-west": _("EU West") + " :flag_eu:",
            "eu-central": _("EU Central") + " :flag_eu:",
            "london": _("London") + " :flag_gb:",
            "frankfurt": _("Frankfurt") + " :flag_de:",
            "amsterdam": _("Amsterdam") + " :flag_nl:",
            "us-west": _("US West") + " :flag_us:",
            "us-east": _("US East") + " :flag_us:",
            "us-south": _("US South") + " :flag_us:",
            "us-central": _("US Central") + " :flag_us:",
            "singapore": _("Singapore") + " :flag_sg:",
            "sydney": _("Sydney") + " :flag_au:",
            "brazil": _("Brazil") + " :flag_br:",
            "hongkong": _("Hong Kong") + " :flag_hk:",
            "russia": _("Russia") + " :flag_ru:",
            "japan": _("Japan") + " :flag_jp:",
            "southafrica": _("South Africa") + " :flag_za:",
            "india": _("India") + " :flag_in:",
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
        em = discord.Embed(
            color=await ctx.embed_colour(), title=_("Servers regions stats:"), description=msg
        )
        em.set_footer(text=_("For a total of {} servers").format(guilds))
        await ctx.send(embed=em)