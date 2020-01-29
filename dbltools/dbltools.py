import discord

from redbot.core import checks, commands, Config
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import bold, box, inline

from typing import Optional, Union

import aiohttp

DBL_BASE_URL = "https://top.gg/api/bots/"

_ = Translator("DblTools", __file__)


@cog_i18n(_)
class DblTools(commands.Cog):
    """Tools to get bots information from Top.gg."""

    __author__ = "Predä"
    __version__ = "1.3.4"

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"

    async def _get_data(self, ctx, bot=None, endpoint: Optional[str] = ""):
        """Get data from Top.gg."""
        key = (await self.bot.get_shared_api_tokens("dbl")).get("api_key")
        headers = {"Authorization": key}
        async with self.session.get(DBL_BASE_URL + str(bot) + endpoint, headers=headers) as resp:
            if resp.status == 401:
                await ctx.send(_("This API key looks wrong, try to set it again."))
                return None
            if resp.status == 404:
                await ctx.send(_("This bot doesn't seem to be validated on Discord Bot List."))
                return None
            if resp.status != 200:
                await ctx.send(
                    _("Error when trying to get Top.gg API. Error code: {}").format(
                        inline(resp.status)
                    )
                )
                return None
            data = await resp.json(content_type=None)
        return data

    @checks.is_owner()
    @commands.command()
    async def dblkey(self, ctx):
        """
            Explain how to set Top.gg API key.

            Note: You need to have a bot published on Top.gg to use API and have a key.
        """
        message = _(
            "So first, to get a Discord Bot List API key, you need "
            "to have a bot on this bot list, otherwise you can't use this cog.\n\n"
            "To find your API key:\n"
            "1. Login on Top.gg [here](https://top.gg/login)\n"
            "2. Go on your [profile](https://top.gg/me)\n"
            "3. Click on `Edit` on one of your bot(s).\n"
            "4. Scroll to the bottom of the edit page, in `API Options` section, "
            "then click on `Show token` and copy the token.\n"
            "5. Use in DM `{}set api dbl api_key,your_api_key_here`\n"
            "6. There you go! You can now use DblTools cog."
        ).format(ctx.prefix)
        await ctx.maybe_send_embed(message)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def dblinfo(self, ctx, *, bot: Union[int, discord.Member, discord.User, None] = None):
        """
            Show information of a chosen bot on Top.gg.

            `[bot]`: Can be a mention or ID of a bot.
        """
        key = (await self.bot.get_shared_api_tokens("dbl")).get("api_key")
        if key is None:
            return await ctx.send(_("Owner of this bot needs to set an API key first !"))
        if bot is None:
            return await ctx.send_help()
        if isinstance(bot, int):
            try:
                bot = await self.bot.fetch_user(bot)
            except discord.NotFound:
                return await ctx.send(str(bot) + _(" is not a Discord user."))
        if not bot.bot:
            return await ctx.send(_("This is not a bot user, please try again with a bot."))

        try:
            async with ctx.typing():
                try:
                    info = await self._get_data(ctx, bot=bot.id)
                    if info is None:
                        return
                    stats = await self._get_data(ctx, endpoint="/stats", bot=bot.id)
                except TypeError:
                    return

                emoji = (
                    discord.utils.get(self.bot.emojis, id=392249976639455232)
                    if self.bot.get_guild(264445053596991498) is not None
                    else "`\N{WHITE HEAVY CHECK MARK}`"
                )
                format_kwargs = {
                    "description": (
                        bold(_("Description:")) + box("\n{}\n").format(info["shortdesc"])
                        if info["tags"]
                        else ""
                    ),
                    "tags": (
                        bold(_("Tags:")) + box("\n{}\n\n").format(", ".join(info["tags"]))
                        if info["tags"]
                        else ""
                    ),
                    "if_cert": (
                        bold(_("\nCertified !")) + f" {emoji}\n" if info["certifiedBot"] else "\n"
                    ),
                    "prefix": (
                        bold(_("Prefix:")) + " {}\n".format(info["prefix"])
                        if info.get("prefix", "")
                        else ""
                    ),
                    "lib": (
                        bold(_("Library:")) + " {}\n".format(info["lib"])
                        if info.get("lib", "")
                        else ""
                    ),
                    "servs": (
                        bold(_("Server count:")) + " {:,}\n".format(stats["server_count"])
                        if stats.get("server_count", "")
                        else ""
                    ),
                    "shards": (
                        bold(_("Shard count:")) + " {:,}\n".format(stats["shard_count"])
                        if stats.get("shard_count", "")
                        else ""
                    ),
                    "m_votes": (
                        bold(_("Monthly votes:"))
                        + (
                            " {:,}\n".format(info["monthlyPoints"])
                            if info.get("monthlyPoints", "")
                            else "0\n"
                        )
                    ),
                    "t_votes": (
                        bold(_("Total votes:"))
                        + (" {:,}\n".format(info["points"]) if info.get("points", "") else "0\n")
                    ),
                    "owners": (
                        bold(_("Owner{}: ").format("s" if len(info["owners"]) > 1 else ""))
                        + ", ".join([str((await self.bot.fetch_user(i))) for i in info["owners"]])
                        + "\n"  # Thanks Slime :ablobcatsipsweats:
                    ),
                    "approval_date": (
                        bold(_("Approval date:"))
                        + " {}\n\n".format(info["date"].replace("T", " ")[:-5])
                    ),
                    "dbl_page": (
                        _("[Top.gg Page]({})").format(f"https://top.gg/bot/{bot.id}")
                    ),
                    "if_inv": (
                        _(" • [Invitation link]({})").format(info["invite"])
                        if info["invite"]
                        else ""
                    ),
                    "if_supp": (
                        _(" • [Support](https://discord.gg/{})").format(info["support"])
                        if info["support"]
                        else ""
                    ),
                    "if_gh": (
                        _(" • [GitHub]({})").format(info["github"]) if info["github"] else ""
                    ),
                    "if_wsite": (
                        _(" • [Website]({})").format(info["website"]) if info["website"] else ""
                    ),
                }
                description = (
                    "{description}"
                    "{tags}"
                    "{if_cert}"
                    "{prefix}"
                    "{lib}"
                    "{servs}{shards}"
                    "{m_votes}"
                    "{t_votes}"
                    "{owners}"
                    "{approval_date}"
                    "{dbl_page}{if_inv}{if_supp}{if_gh}{if_wsite}"
                ).format(**format_kwargs)
                em = discord.Embed(color=(await ctx.embed_colour()), description=description)
                em.set_author(
                    name=_("Top.gg Info about {}:").format(info["username"]),
                    icon_url="https://cdn.discordapp.com/emojis/393548388664082444.gif",
                )
                em.set_thumbnail(url=bot.avatar_url_as(static_format="png"))
                return await ctx.send(embed=em)
        except Exception as error:
            return await ctx.send(
                _("Something went wrong when trying to get bot information.\n")
                + inline(str(error))
            )

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def dblwidget(self, ctx, *, bot: Union[int, discord.Member, discord.User, None] = None):
        """Send the widget of a chosen bot on Top.gg."""
        key = (await self.bot.get_shared_api_tokens("dbl")).get("api_key")
        if key is None:
            return await ctx.send(_("Owner of this bot need to set an API key first !"))
        if bot is None:
            return await ctx.send_help()
        if isinstance(bot, int):
            try:
                bot = await self.bot.fetch_user(bot)
            except discord.NotFound:
                return await ctx.send(str(bot) + _(" is not a Discord user."))
        if not bot.bot:
            return await ctx.send(_("This is not a bot user, please try again with a bot."))

        async with ctx.typing():
            data = await self._get_data(ctx, bot=bot.id)
            if data is None:
                return
            em = discord.Embed(
                color=discord.Color.blurple(),
                description=bold(_("[Top.gg Page]({})")).format(
                    f"https://top.gg/bot/{bot.id}"
                ),
            )
            em.set_image(url=f"https://top.gg/api/widget/{bot.id}.png")
        await ctx.send(embed=em)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
