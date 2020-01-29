import discord

import aiohttp
import json

from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import bold, box, inline

from random import choice
from typing import Optional

from .constants import REDDIT_BASEURL, IMGUR_LINKS, GOOD_EXTENSIONS, Stuff

_ = Translator("Nsfw", __file__)


@cog_i18n(_)
class Core(Stuff):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    async def _get_imgs(self, ctx, sub=None):
        """Get images from Reddit API."""
        try:
            async with self.session.get(REDDIT_BASEURL.format(choice(sub))) as reddit:
                if reddit.status != 200:
                    await self._api_errors_msg(ctx, error_code=reddit.status)
                    return None, None
                try:
                    data = await reddit.json(content_type=None)
                    content = data[0]["data"]["children"][0]["data"]
                    url = content["url"]
                    subr = content["subreddit"]
                except (KeyError, ValueError, json.decoder.JSONDecodeError):
                    url, subr = await self._get_imgs(ctx, sub=sub)
                if url.startswith(IMGUR_LINKS):
                    url = url + ".png"
                elif url.endswith(".mp4"):
                    url = url[:-3] + "gif"
                elif url.endswith(".gifv"):
                    url = url[:-1]
                elif not url.endswith(GOOD_EXTENSIONS) and not url.startswith(
                    "https://gfycat.com"
                ):
                    url, subr = await self._get_imgs(ctx, sub=sub)
                return url, subr
        except aiohttp.client_exceptions.ClientConnectionError:
            await self._api_errors_msg(ctx, error_code="JSON decode failed")
            return None, None

    async def _get_others_imgs(self, ctx, url=None):
        """Get images from all other images APIs."""
        try:
            async with self.session.get(url) as resp:
                if resp.status != 200:
                    await self._api_errors_msg(ctx, error_code=resp.status)
                    return None
                try:
                    data = await resp.json(content_type=None)
                except json.decoder.JSONDecodeError as exception:
                    await self._api_errors_msg(ctx, error_code=exception)
                    return None
            data = dict(img=data)
            return data
        except aiohttp.client_exceptions.ClientConnectionError:
            await self._api_errors_msg(ctx, error_code="JSON decode failed")
            return None

    async def _api_errors_msg(self, ctx, error_code=None):
        """Error message when API calls fail."""
        return await ctx.send(
            _("Error when trying to contact image service, please try again later. ")
            + "(Code: {})".format(inline(str(error_code)))
        )

    async def _version_msg(self, ctx, version, authors):
        """Cog version message."""
        msg = box(
            _("Nsfw cog version: {version}\nAuthors: {authors}").format(
                version=version, authors=", ".join(authors)
            ),
            lang="py",
        )
        return await ctx.send(msg)

    async def _make_embed(self, ctx, sub, name):
        """Function to make the embed for all Reddit API images."""
        url, subr = await self._get_imgs(ctx, sub=sub)
        if not url:
            return
        if url.endswith(GOOD_EXTENSIONS):
            em = await self._embed(
                color=0x891193,
                title=(_("Here is {name} image ...") + " \N{EYES}").format(name=name),
                description=bold(_("[Link if you don't see image]({url})")).format(url=url),
                image=url,
                footer=_("Requested by {req} {emoji} • From r/{r}").format(
                    req=ctx.author.display_name, emoji=await self.emoji(), r=subr
                ),
            )
        if url.startswith("https://gfycat.com"):
            em = (
                _("Here is {name} gif ...")
                + " \N{EYES}\n\n"
                + _("Requested by {req} {emoji} • From {r}\n{url}")
            ).format(
                name=name,
                req=bold(ctx.author.display_name),
                emoji=await self.emoji(),
                r=bold(f"r/{subr}"),
                url=url,
            )
        return em

    async def _make_embed_other(self, ctx, name, url, arg, source):
        """Function to make the embed for all others APIs images."""
        data = await self._get_others_imgs(ctx, url=url)
        if not data:
            return
        em = await self._embed(
            color=0x891193,
            title=(_("Here is {name} image ...") + " \N{EYES}").format(name=name),
            description=bold(_("[Link if you don't see image]({url})")).format(
                url=data["img"][arg]
            ),
            image=data["img"][arg],
            footer=_("Requested by {req} {emoji} • From {source}").format(
                req=ctx.author.display_name, emoji=await self.emoji(), source=source
            ),
        )
        return em

    async def _maybe_embed(self, ctx, embed):
        """
            Function to choose if type of the message is an embed or not
            and if not send a simple message.
        """
        try:
            if isinstance(embed, discord.Embed):
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed)
        except discord.HTTPException:
            return

    async def _send_msg(self, ctx, name, sub=None):
        """Main function called in all Reddit API commands."""
        async with ctx.typing():
            embed = await self._make_embed(ctx, sub, name)
        return await self._maybe_embed(ctx, embed=embed)

    async def _send_other_msg(self, ctx, name, arg, source, url=None):
        """Main function called in all others APIs commands."""
        async with ctx.typing():
            embed = await self._make_embed_other(ctx, name, url, arg, source)
        return await self._maybe_embed(ctx, embed)

    @staticmethod
    async def _embed(
        color=None, title=None, description=None, image=None, footer: Optional[str] = None
    ):
        em = discord.Embed(color=color, title=title, description=description)
        em.set_image(url=image)
        if footer:
            em.set_footer(text=footer)
        return em


def nsfwcheck():
    """
        Custom check that hide all commands used with it in the help formatter
        and block usage of them if used in a non-nsfw channel.
    """

    async def predicate(ctx):
        if not ctx.guild:
            return True
        if ctx.message.channel.is_nsfw():
            return True
        if ctx.invoked_with == "help" and not ctx.message.channel.is_nsfw():
            return False
        if ctx.invoked_with not in [k for k in ctx.bot.all_commands]:
            # For this weird issue with last version of discord.py (1.2.3) with non-existing commands.
            # So this check is only for dev version of Red.
            # https://discordapp.com/channels/133049272517001216/133251234164375552/598149067268292648 for reference.
            # It probably need to check in d.py to see what is happening, looks like an issue somewhere.
            # It will probably removed in the future, it's a temporary check.
            return False
        msg = _("You can't use this command in a non-NSFW channel !")
        try:
            embed = discord.Embed(title="\N{LOCK} " + msg, color=0xAA0000)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(msg)
        finally:
            return False

    return commands.check(predicate)
