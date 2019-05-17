import discord

from redbot.core import checks, commands, Config
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import bold, box, inline

from typing import Union

import aiohttp

DBL_BASE_URL = "https://discordbots.org/api/bots/"

_ = Translator("DblTools", __file__)


@cog_i18n(_)
class DblTools(commands.Cog):
    """Tools to get bots information from discordbots.org."""

    __author__ = "Predä"
    __version__ = "1.1.1"

    def __init__(self, bot):
        defaut = {"dbl_key": None}
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.config = Config.get_conf(self, 3329804706503720961, force_registration=True)
        self.config.register_global(**defaut)

    # This part of code is originally from image.py of Red, I take it because it's amazing:
    # https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/cogs/image/image.py#L30
    async def initialize(self) -> None:
        """Move the API keys from cog stored config to core bot config if they exist."""
        dbl_key = await self.config.dbl_key()
        if dbl_key is not None and "dbl" not in await self.bot.db.api_tokens():
            await self.bot.db.api_tokens.set_raw("dbl", value={"api_key": dbl_key})
            await self.config.dbl_key.clear()

    async def _get_info(self, ctx, bot=None, info=None, stats=None):
        """Get info from discordbots.org."""
        key = await ctx.bot.db.api_tokens.get_raw("dbl", default=None)
        headers = {"Authorization": key["api_key"]}
        async with self.session.get(DBL_BASE_URL + str(bot), headers=headers) as resp:
            if resp.status == 401:
                await ctx.send(_("This API key looks wrong, try to set it again."))
                return None
            if resp.status == 404:
                await ctx.send(_("This bot doesn't seem to be validated on Discord Bot List."))
                return None
            if resp.status != 200:
                await ctx.send(
                    "Error when trying to get DBL API. Error code: {}".format(inline(resp.status))
                )
                return None
            info = await resp.json(content_type=None)
        async with self.session.get(DBL_BASE_URL + str(bot) + "/stats", headers=headers) as resp:
            if resp.status != 200:
                return None
            stats = await resp.json(content_type=None)
        return info, stats

    @checks.is_owner()
    @commands.command()
    async def dblkey(self, ctx):
        """
            Explain how to set DBL API key.

            Note: You need to have a bot published on DBL to use API and have a key.
        """
        message = _(
            "So first, to get a Discord Bot List API key, you need "
            "to have a bot on this bot list, otherwise you can't use this cog.\n\n"
            "To find your API key:\n"
            "1. Login on DBL [here](https://discordbots.org/login)\n"
            "2. Go on your [profile](https://discordbots.org/me)\n"
            "3. Click on `Edit` on one of your bot(s).\n"
            "4. Scroll to the bottom of the edit page, in `API Options` section, "
            "then click on `Show token` and copy the token.\n"
            "5. Use in DM `{}set api dbl api_key,your_api_key_here`\n"
            "6. There you go! You can now use DblTools cog."
        ).format(ctx.prefix)
        await ctx.maybe_send_embed(message)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def dblinfo(self, ctx, *, bot: Union[int, discord.Member, discord.User, None] = None):
        """
            Show information of a chosen bot on discordbots.org.

            `[bot]`: Can be a mention or ID of a bot.
        """
        key = await ctx.bot.db.api_tokens.get_raw("dbl", default=None)
        if key is None:
            return await ctx.send(_("Owner of this bot need to set an API key first !"))
        if bot is None:
            return await ctx.send_help()
        if isinstance(bot, int):
            try:
                bot = await self.bot.get_user_info(bot)
            except discord.errors.NotFound:
                return await ctx.send(str(bot) + _(" is not a Discord user."))

        try:
            async with ctx.typing():
                try:
                    info, stats = await self._get_info(ctx, bot=bot.id, info=None, stats=None)
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
                        + (
                            " {:,}\n\n".format(info["points"])
                            if info.get("points", "")
                            else "0\n\n"
                        )
                    ),
                    "dbl_page": (
                        _("[DBL Page]({})").format(f"https://discordbots.org/bot/{bot.id}")
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
                    "{dbl_page}{if_inv}{if_supp}{if_gh}{if_wsite}"
                ).format(**format_kwargs)
                em = discord.Embed(color=(await ctx.embed_colour()), description=description)
                em.set_author(
                    name=_("DBL Stats of {}:").format(info["username"]),
                    icon_url="https://cdn.discordapp.com/emojis/393548388664082444.gif",
                )
                em.set_thumbnail(url=bot.avatar_url_as(static_format="png"))
                return await ctx.send(embed=em)
        except Exception as error:
            return await ctx.send(
                _("It doesn't seem to be a valid ID. Try again or check if the ID is right.\n")
                + inline(str(error))
            )

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
