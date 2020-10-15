import discord
from redbot.core.bot import Red
from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import (
    bold,
    box,
    humanize_number,
    pagify,
)
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

import dbl
import time
import math
import aiohttp
import asyncio
from tabulate import tabulate
from collections import Counter

from .utils import download_widget


_ = Translator("DblTools", __file__)


@cog_i18n(_)
class DblToolsLite(commands.Cog):
    """Tools for Top.gg API."""

    __author__ = "Predä"
    __version__ = "2.0.2_lite"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def __init__(self, bot: Red):
        self.bot = bot
        self.dbl = None

        self.session = aiohttp.ClientSession()
        self._init_task = bot.loop.create_task(self.initialize())
        self._ready_event = asyncio.Event()

    async def initialize(self):
        await self.bot.wait_until_ready()
        key = (await self.bot.get_shared_api_tokens("dbl")).get("api_key")
        try:
            client = dbl.DBLClient(self.bot, key, session=self.session)
            await client.get_guild_count()
        except (dbl.Unauthorized, dbl.UnauthorizedDetected):
            await client.close()
            return await self.bot.send_to_owners("Failed to load DblTools cog. Wrong token.")
        except dbl.NotFound:
            await client.close()
            return await self.bot.send_to_owners("Failed to load DblTools cog. Not validated bot.")
        self.dbl = client
        self._ready_event.set()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
        if self._init_task:
            self._init_task.cancel()

    async def cog_before_invoke(self, ctx: commands.Context):
        await self._ready_event.wait()

    @commands.command(aliases=["dblinfo"])
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def topgginfo(self, ctx: commands.Context, *, bot: discord.User = None):
        """
        Show information of a chosen bot on Top.gg.
        `bot`: Can be a mention or ID of a bot.
        """
        if bot is None:
            bot = self.bot.user
        if not bot.bot:
            return await ctx.send(_("This is not a bot user, please try again with a bot."))

        async with ctx.typing():
            try:
                data = await self.dbl.get_bot_info(bot.id)
            except dbl.NotFound:
                return await ctx.send(_("That bot isn't validated on Top.gg."))
            except dbl.errors.HTTPException as error:
                return await ctx.send(_("Failed to contact Top.gg API. Please try again later."))

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
            except dbl.errors.HTTPException as error:
                log.error("Failed to fetch Top.gg API.", exc_info=error)
                return await ctx.send(_("Failed to contact Top.gg API. Please try again later."))
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
        try:
            data = await self.dbl.get_bot_upvotes()
        except dbl.errors.HTTPException as error:
            log.error("Failed to fetch Top.gg API.", exc_info=error)
            return await ctx.send(_("Failed to contact Top.gg API. Please try again later."))
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
