import discord
from redbot.core.bot import Red
from redbot.core.i18n import Translator, cog_i18n
from redbot.core import bank, commands, Config, checks, errors
from redbot.core.utils.chat_formatting import (
    bold,
    box,
    humanize_number,
    humanize_timedelta,
    pagify,
)
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

import dbl
import time
import math
import aiohttp
import logging
import asyncio
import calendar
from typing import Mapping
from tabulate import tabulate
from collections import Counter
from datetime import datetime, timedelta

from .utils import check_weekend, download_widget, error_message, guild_only_check, intro_msg


log = logging.getLogger("red.predacogs.DblTools")
_ = Translator("DblTools", __file__)


@cog_i18n(_)
class DblTools(commands.Cog):
    """Tools for Top.gg API."""

    __author__ = "Predä"
    __version__ = "2.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.dbl = None

        self.config = Config.get_conf(
            self, identifier=51222797489301095423, force_registration=True
        )
        self.config.register_global(
            post_guild_count=False,
            support_server_role={"guild_id": None, "role_id": None},
            daily_rewards={
                "toggled": False,
                "amount": 100,
                "weekend_bonus_toggled": False,
                "weekend_bonus_amount": 500,
            },
        )
        self.config.register_user(next_daily=0)

        self.economy_cog = None
        self.session = aiohttp.ClientSession()
        self._init_task = bot.loop.create_task(self.initialize())
        self._post_stats_task = self.bot.loop.create_task(self.update_stats())
        self._ready_event = asyncio.Event()

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"

    async def initialize(self):
        await self.bot.wait_until_ready()
        key = (await self.bot.get_shared_api_tokens("dbl")).get("api_key")
        try:
            client = dbl.DBLClient(self.bot, key, session=self.session)
            await client.get_guild_count()
        except (dbl.Unauthorized, dbl.UnauthorizedDetected):
            await client.close()
            return await self.bot.send_to_owners(
                "[DblTools cog]\n" + error_message.format(intro_msg)
            )
        except dbl.NotFound:
            await client.close()
            return await self.bot.send_to_owners(
                _(
                    "[DblTools cog]\nThis bot seems doesn't seems be validated on Top.gg. Please try again with a validated bot."
                )
            )
        self.dbl = client
        self._ready_event.set()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
        if self._init_task:
            self._init_task.cancel()
        if self._post_stats_task:
            self._post_stats_task.cancel()

    async def cog_before_invoke(self, ctx: commands.Context):
        await self._ready_event.wait()

    async def update_stats(self):
        await self.bot.wait_until_ready()
        if await self.config.post_guild_count():
            try:
                await self.dbl.post_guild_count()
                log.info(
                    "Posted server count to Top.gg {} servers.".format(self.dbl.guild_count())
                )
            except Exception as error:
                log.exception(
                    "Failed to post server count\n{}: {}".format(type(error).__name__, error)
                )
            await asyncio.sleep(1800)

    @commands.Cog.listener()
    async def on_red_api_tokens_update(self, service_name: str, api_tokens: Mapping[str, str]):
        if service_name != "dbl":
            return
        try:
            if self.dbl:
                self.dbl.close()
            client = dbl.DBLClient(self.bot, api_tokens.get("api_key"), session=self.session)
            await client.get_guild_count()
        except (dbl.Unauthorized, dbl.UnauthorizedDetected):
            await client.close()
            return await self.bot.send_to_owners(
                "[DblTools cog]\n"
                + error_message.format(_("A wrong token has been set for dbltools cog.\n\n"))
            )
        except dbl.NotFound:
            await client.close()
            return await self.bot.send_to_owners(
                _(
                    "[DblTools cog]\nThis bot seems doesn't seems be validated on Top.gg. Please try again with a validated bot."
                )
            )
        self.dbl = client
        self._ready_event.set()

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self.bot.wait_until_ready()
        await self._ready_event.wait()
        config = await self.config.all()
        if not member.guild.id == config["support_server_role"]["guild_id"]:
            return
        if not config["support_server_role"]["role_id"]:
            return
        if await self.dbl.get_user_vote(member.id):
            try:
                await member.add_roles(
                    member.guild.get_role(config["support_server_role"]["role_id"]),
                    reason=f"Top.gg {self.bot.user.name} upvoter.",
                )
            except discord.Forbidden:
                await self.bot.send_to_owners(
                    _(
                        "It seems that I no longer have permissions to add roles for Top.gg upvoters "
                        "in {} `{}`. Role rewards has been disabled."
                    ).format(member.guild, member.guild.id)
                )
                async with self.config.all() as config:
                    config["support_server_role"]["guild_id"] = None
                    config["support_server_role"]["role_id"] = None

    @commands.group()
    async def dblset(self, ctx: commands.Context):
        """Group commands for settings of DblTools cog."""

    @dblset.command()
    @checks.is_owner()
    async def poststats(self, ctx: commands.Context):
        """Set if you want to send your bot stats (Guilds and shards count) to Top.gg API."""
        toggled = await self.config.post_guild_count()
        await self.config.post_guild_count.set(not toggled)
        msg = _("Daily command enabled.") if not toggled else _("Daily command disabled.")
        await ctx.send(msg)

    @dblset.group(aliases=["rolereward"])
    @commands.guild_only()
    async def rolerewards(self, ctx: commands.Context):
        """Settings for role rewards."""

    @rolerewards.command()
    @commands.bot_has_permissions(manage_roles=True)
    async def role(self, ctx: commands.Context, *, role: discord.Role):
        """Set the role that will be added to new users if they have upvoted for your bot."""
        async with self.config.all() as config:
            config["support_server_role"]["guild_id"] = ctx.guild.id
            config["support_server_role"]["role_id"] = role.id
        await ctx.send(_("Role reward has been enabled and set to: `{}`").format(role.name))

    @rolerewards.command()
    async def reset(self, ctx: commands.Context):
        """Reset current role rewards setup."""
        async with self.config.all() as config:
            config["support_server_role"]["guild_id"] = None
            config["support_server_role"]["role_id"] = None
        await ctx.tick()

    @dblset.group(aliases=["dailyreward"])
    async def dailyrewards(self, ctx: commands.Context):
        """Settings for daily rewards."""

    @dailyrewards.command()
    async def toggle(self, ctx: commands.Context):
        """Set wether you want [p]daily command usable or not."""
        toggled = await self.config.daily_rewards.get_raw("toggled")
        await self.config.daily_rewards.set_raw("toggled", value=not toggled)
        msg = _("Daily command enabled.") if not toggled else _("Daily command disabled.")
        await ctx.send(msg)

    @dailyrewards.command()
    async def amount(self, ctx: commands.Context, amount: int = None):
        """Set the amount of currency that users will receive on daily rewards."""
        if not amount:
            return await ctx.send_help()
        if amount >= await bank.get_max_balance():
            return await ctx.send(_("The amount needs to be lower than bank maximum balance."))
        await self.config.daily_rewards.set_raw("amount", value=amount)
        await ctx.send(_("Daily rewards amount set to {}").format(amount))

    @dailyrewards.command()
    async def weekend(self, ctx: commands.Context):
        """Set weekend bonus."""
        toggled = await self.config.daily_rewards.get_raw("weekend_bonus_toggled")
        await self.config.daily_rewards.set_raw("weekend_bonus_toggled", value=not toggled)
        msg = _("Weekend bonus enabled.") if not toggled else _("Weekend bonus disabled.")
        await ctx.send(msg)

    @dailyrewards.command()
    async def weekendamount(self, ctx: commands.Context, amount: int = None):
        """Set the amount of currency that users will receive on week-end bonus."""
        if not amount:
            return await ctx.send_help()
        if amount >= await bank.get_max_balance():
            return await ctx.send(_("The amount needs to be lower than bank maximum balance."))
        await self.config.daily_rewards.set_raw("weekend_bonus_amount", value=amount)
        await ctx.send(_("Weekend bonus amount set to {}").format(amount))

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def dblinfo(self, ctx: commands.Context, *, bot: discord.User):
        """
        Show information of a chosen bot on Top.gg.

        `bot`: Can be a mention or ID of a bot.
        """
        if bot is None:
            return await ctx.send(_("This is not a valid Discord user."))
        if not bot.bot:
            return await ctx.send(_("This is not a bot user, please try again with a bot."))

        async with ctx.typing():
            try:
                data = await self.dbl.get_bot_info(bot.id)
            except dbl.NotFound:
                return await ctx.send(_("That bot isn't validated on Top.gg."))

            cert_emoji = (
                "<:dblCertified:392249976639455232>"
                if self.bot.get_guild(264445053596991498)
                else "\N{WHITE HEAVY CHECK MARK}"
            )
            fields = {
                "description": (
                    bold(_("Description:")) + box("\n{}\n").format(data["shortdesc"])
                    if data["shortdesc"]
                    else ""
                ),
                "tags": (
                    bold(_("Tags:")) + box("\n{}\n\n").format(", ".join(data["tags"]))
                    if data["tags"]
                    else ""
                ),
                "certified": (
                    bold(_("\nCertified!")) + f" {cert_emoji}\n" if data["certifiedBot"] else "\n"
                ),
                "prefixes": (
                    bold(_("Prefix:")) + " {}\n".format(data["prefix"])
                    if data.get("prefix")
                    else ""
                ),
                "library": (
                    bold(_("Library:")) + " {}\n".format(data["lib"]) if data.get("lib") else ""
                ),
                "servers": (
                    bold(_("Server count:"))
                    + " {}\n".format(humanize_number(data["server_count"]))
                    if data.get("server_count")
                    else ""
                ),
                "shards": (
                    bold(_("Shard count:")) + " {}\n".format(humanize_number(data["shard_count"]))
                    if data.get("shard_count")
                    else ""
                ),
                "votes_month": (
                    bold(_("Monthly votes:"))
                    + (" {}\n".format(humanize_number(data.get("monthlyPoints", 0))))
                ),
                "votes_total": (
                    bold(_("Total votes:"))
                    + (" {}\n".format(humanize_number(data.get("points", 0))))
                ),
                "owners": (
                    bold("{}: ").format(_("Owners") if len(data["owners"]) > 1 else _("Owner"))
                    + ", ".join([str((self.bot.get_user(int(u)))) for u in data["owners"]])
                    + "\n"  # Thanks Slime :ablobcatsipsweats:
                ),
                "approval_date": (
                    bold(_("Approval date:")) + " {}\n\n".format(str(data["date"]).split(".")[0])
                ),
                "dbl_page": _("[Top.gg Page]({})").format(f"https://top.gg/bot/{bot.id}"),
                "invitation": (
                    _(" • [Invitation link]({})").format(data["invite"])
                    if data.get("invite")
                    else ""
                ),
                "support_server": (
                    _(" • [Support](https://discord.gg/{})").format(data["support"])
                    if data.get("support")
                    else ""
                ),
                "github": (
                    _(" • [GitHub]({})").format(data["github"]) if data.get("github") else ""
                ),
                "website": (
                    _(" • [Website]({})").format(data["website"]) if data.get("website") else ""
                ),
            }
            description = [field for field in list(fields.values())]
            em = discord.Embed(color=(await ctx.embed_colour()), description="".join(description))
            em.set_author(
                name=_("Top.gg info about {}:").format(data["username"]),
                icon_url="https://cdn.discordapp.com/emojis/393548388664082444.gif",
            )
            em.set_thumbnail(url=bot.avatar_url_as(static_format="png"))
            return await ctx.send(embed=em)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def dblwidget(self, ctx: commands.Context, *, bot: discord.User):
        """
        Send the widget of a chosen bot on Top.gg.

        `bot`: Can be a mention or ID of a bot.
        """
        if bot is None:
            return await ctx.send(_("This is not a valid Discord user."))
        if not bot.bot:
            return await ctx.send(_("This is not a bot user, please try again with a bot."))

        async with ctx.typing():
            try:
                await self.dbl.get_guild_count(bot.id)
                url = await self.dbl.get_widget_large(bot.id)
            except dbl.NotFound:
                return await ctx.send(_("That bot isn't validated on Top.gg."))
            file = await download_widget(self.session, url)
            em = discord.Embed(
                color=discord.Color.blurple(),
                description=bold(_("[Top.gg Page]({})")).format(f"https://top.gg/bot/{bot.id}"),
            )
            if file:
                filename = f"{bot.id}_topggwidget_{int(time.time())}.png"
                em.set_image(url=f"attachment://{filename}")
                return await ctx.send(file=discord.File(file, filename=filename), embed=em)
            em.set_image(url=url)
            return await ctx.send(embed=em)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def listdblvotes(self, ctx: commands.Context):
        """Sends a list of the persons who voted for the bot this month."""
        data = await self.dbl.get_bot_upvotes()
        if not data:
            return await ctx.send(_("Your bot hasn't received any votes yet."))

        votes_count = Counter()
        for user_data in data:
            votes_count[user_data["id"]] += 1
        votes = []
        for user_id, value in votes_count.most_common():
            user = self.bot.get_user(int(user_id))
            votes.append((user if user else user_id, humanize_number(value)))
        msg = tabulate(votes, tablefmt="orgtbl")
        embeds = []
        pages = 1
        for page in pagify(msg, delims=["\n"], page_length=1300):
            em = discord.Embed(
                color=await ctx.embed_color(),
                title=_("Monthly votes of {}:").format(self.bot.user),
                description=box(page),
            )
            em.set_footer(
                text=_("Page {}/{}").format(
                    humanize_number(pages), humanize_number((math.ceil(len(msg) / 1300)))
                )
            )
            pages += 1
            embeds.append(em)
        if len(embeds) > 1:
            await menu(ctx, embeds, DEFAULT_CONTROLS)
        else:
            await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def dailyreward(self, ctx: commands.Context):
        """Claim your daily reward."""
        config = await self.config.all()
        if not config["daily_rewards"]["toggled"]:
            return
        author = ctx.author
        cur_time = int(time.time())
        next_daily = await self.config.user(author).next_daily()
        if cur_time <= next_daily:
            delta = humanize_timedelta(seconds=next_daily - cur_time) or "1 second"
            msg = author.mention + _(
                " Too soon!\nYou have already claim your daily reward!\n"
                "Wait **{}** for the next one."
            ).format(delta)
            if not await ctx.embed_requested():
                await ctx.send(msg)
            else:
                em = discord.Embed(description=msg, color=discord.Color.red())
                await ctx.send(embed=em)
            return
        credits_name = await bank.get_currency_name(ctx.guild)
        weekend = check_weekend() and config["daily_rewards"]["weekend_bonus_toggled"]
        if not await self.dbl.get_user_vote(author.id):
            maybe_weekend_bonus = ""
            if weekend:
                maybe_weekend_bonus = _(" and the week-end bonus of {} {}").format(
                    humanize_number(config["daily_rewards"]["weekend_bonus_amount"]), credits_name
                )
            title = _(
                "**Click here to upvote {bot_name} every 12 hours to earn {amount} {currency}{weekend}!**"
            ).format(
                bot_name=self.bot.user.name,
                amount=humanize_number(config["daily_rewards"]["amount"]),
                currency=credits_name,
                weekend=maybe_weekend_bonus,
            )
            vote_url = f"https://top.gg/bot/{self.bot.user.id}/vote"
            if not await ctx.embed_requested():
                await ctx.send(f"{title}\n\n{vote_url}")
            else:
                em = discord.Embed(color=discord.Color.red(), title=title, url=vote_url)
                await ctx.send(embed=em)
            return
        regular_amount = config["daily_rewards"]["amount"]
        weekend_amount = config["daily_rewards"]["weekend_bonus_amount"]
        next_vote = int(datetime.timestamp(datetime.now() + timedelta(hours=12)))
        try:
            await bank.deposit_credits(
                author, amount=regular_amount + weekend_amount if weekend else regular_amount
            )
        except errors.BalanceTooHigh as exc:
            await bank.set_balance(author, exc.max_balance)
            await ctx.send(
                _(
                    "You've reached the maximum amount of {currency}! (**{new_balance}**) "
                    "Please spend some more \N{GRIMACING FACE}\n\n"
                    "You currently have {new_balance} {currency}."
                ).format(currency=credits_name, new_balance=humanize_number(exc.max_balance))
            )
            return

        pos = await bank.get_leaderboard_position(author)
        await self.config.user(author).next_daily.set(next_vote)
        maybe_weekend_bonus = (
            _("\nAnd your week-end bonus, +{}!").format(humanize_number(weekend_amount))
            if weekend
            else ""
        )
        title = _("Here is your daily bonus!")
        description = _(
            " Take some {currency}. Enjoy! (+{amount} {currency}!){weekend}\n\n"
            "You currently have {new_balance} {currency}.\n\n"
        ).format(
            currency=credits_name,
            amount=humanize_number(regular_amount),
            weekend=maybe_weekend_bonus,
            new_balance=humanize_number(await bank.get_balance(author)),
        )
        footer = _("You are currently #{} on the global leaderboard!").format(humanize_number(pos))
        if not await ctx.embed_requested():
            await ctx.send(f"{author.mention} {title}{description}\n\n{footer}")
        else:
            em = discord.Embed(
                color=await ctx.embed_color(),
                title=title,
                description=author.mention + description,
            )
            em.set_footer(text=footer)
            await ctx.send(embed=em)
