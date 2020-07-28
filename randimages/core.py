import discord

from redbot.core.bot import Red
from redbot.core import Config, commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import bold, box, inline

import json
import asyncio
import aiohttp
from random import choice
from typing import Optional, Union

from .constants import REDDIT_BASEURL, IMGUR_LINKS, GOOD_EXTENSIONS

_ = Translator("Image", __file__)

# TODO Needs a good rewrite and simplification.
# TODO Implement the possibility to use my API as an option untoggled by default.


@cog_i18n(_)
class Core(commands.Cog):

    __author__ = "Predä"
    __version__ = "1.1.9"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def __init__(self, bot: Red):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"

    async def _get_reddit_imgs_simple(self, ctx: commands.Context, sub: list):
        """Get images from Reddit API."""
        try:
            async with self.session.get(REDDIT_BASEURL.format(choice(sub))) as reddit:
                if reddit.status == 404:
                    await ctx.send(_("This is not a valid subreddit."))
                    return None, None
                if reddit.status != 200:
                    await self._api_errors_msg(ctx, error_code=reddit.status)
                    return None, None
                try:
                    data = await reddit.json(content_type=None)
                    content = data[0]["data"]["children"][0]["data"]
                    url = content["url"]
                    subr = content["subreddit"]
                    nsfw = content["over_18"]
                    if ctx.guild and nsfw and not ctx.message.channel.is_nsfw():
                        await ctx.send(embed=await self._nsfw_channel_check(ctx))
                        return None, None
                except (KeyError, ValueError, json.decoder.JSONDecodeError):
                    url, subr = await self._get_reddit_imgs_simple(ctx, sub=sub)
                if url.startswith(IMGUR_LINKS):
                    url = url + ".png"
                elif url.endswith(".mp4"):
                    url = url[:-3] + "gif"
                elif url.endswith(".gifv"):
                    url = url[:-1]
                elif not url.endswith(GOOD_EXTENSIONS) and not url.startswith(
                    "https://gfycat.com"
                ):
                    url, subr = await self._get_reddit_imgs_simple(ctx, sub=sub)
                return url, subr
        except aiohttp.client_exceptions.ClientConnectionError:
            await self._api_errors_msg(ctx, error_code="JSON decode failed")
            return None, None

    async def _get_reddit_imgs_details(self, ctx: commands.Context, sub: list):
        """Get images from Reddit API with more details."""
        try:
            async with self.session.get(REDDIT_BASEURL.format(choice(sub))) as reddit:
                if reddit.status == 404:
                    await ctx.send(_("This is not a valid subreddit."))
                    return None, None, None, None, None
                if reddit.status != 200:
                    await self._api_errors_msg(ctx, error_code=reddit.status)
                    return None, None, None, None, None
                try:
                    data = await reddit.json(content_type=None)
                    content = data[0]["data"]["children"][0]["data"]
                    author = content["author"]
                    title = content["title"]
                    url = content["url"]
                    subr = content["subreddit"]
                    nsfw = content["over_18"]
                    permalink = content["permalink"]
                    text = content["selftext"]
                    post = f"https://www.reddit.com{permalink}"
                    if ctx.guild and nsfw and not ctx.message.channel.is_nsfw():
                        await ctx.send(embed=await self._nsfw_channel_check(ctx))
                        return None, None, None, None, None
                except (KeyError, ValueError, json.decoder.JSONDecodeError):
                    url, subr, author, title, post = await self._get_reddit_imgs_details(
                        ctx, sub=sub
                    )
                if url.startswith(IMGUR_LINKS):
                    url = url + ".png"
                elif url.endswith(".mp4"):
                    url = url[:-3] + "gif"
                elif url.endswith(".gifv"):
                    url = url[:-1]
                elif (
                    text
                    or not url.endswith(GOOD_EXTENSIONS)
                    and not url.startswith("https://gfycat.com")
                ):
                    url, subr, author, title, post = await self._get_reddit_imgs_details(
                        ctx, sub=sub
                    )
            return url, subr, author, title, post
        except aiohttp.client_exceptions.ClientConnectionError:
            await self._api_errors_msg(ctx, error_code="JSON decode failed")
            return None, None, None, None, None

    async def _get_others_imgs(
        self,
        ctx: commands.Context,
        facts: bool,
        img_url: str = None,
        facts_url: Optional[str] = None,
    ):
        """Get images from all other images APIs and facts if needed."""
        try:
            async with self.session.get(img_url) as resp:
                fact_data = None
                if resp.status != 200:
                    await self._api_errors_msg(ctx, error_code=resp.status)
                    return None
                try:
                    img_data = await resp.json(content_type=None)
                except json.decoder.JSONDecodeError as exception:
                    await self._api_errors_msg(ctx, error_code=exception)
                    return None
            if facts:
                async with self.session.get(facts_url) as resp:
                    if resp.status != 200:
                        await self._api_errors_msg(ctx, error_code=resp.status)
                        return None
                    try:
                        fact_data = await resp.json(content_type=None)
                    except json.decoder.JSONDecodeError as exception:
                        await self._api_errors_msg(ctx, error_code=exception)
                        return None
            data = dict(img=img_data, fact=fact_data)
            return data
        except aiohttp.client_exceptions.ClientConnectionError:
            await self._api_errors_msg(ctx, error_code="JSON decode failed")
            return None

    async def _api_errors_msg(self, ctx: commands.Context, error_code: int):
        """Error message when API calls fail."""
        return await ctx.send(
            _("Error when trying to contact image service, please try again later. ")
            + "(Code: {})".format(inline(str(error_code)))
        )

    async def _nsfw_channel_check(self, ctx: commands.Context):
        """Message for non-nsfw channels."""
        if not ctx.message.channel.is_nsfw():
            em = discord.Embed(
                title="\N{LOCK} " + _("NSFW content in the link. Blocked in non-NSFW channel."),
                color=0xAA0000,
            )
        return em

    async def _make_embed_reddit_simple(
        self, ctx: commands.Context, sub: str, name: str, emoji: str
    ):
        """Function to make the embed for all Reddit API images."""
        try:
            url, subr = await asyncio.wait_for(self._get_reddit_imgs_simple(ctx, sub=sub), 3)
        except asyncio.TimeoutError:
            await ctx.send(
                "Failed to get an image.\n"
                "(Timeout error, it most likely means that Reddit API haven't returned images for 3 seconds)"
            )
            return
        if not url:
            return
        em = ""  # FIXME That thing is dumb.
        if url.endswith(GOOD_EXTENSIONS):
            em = await self._embed(
                color=await ctx.embed_colour(),
                title=(_("Here is {name} ... ") + emoji).format(name=name),
                description=bold(
                    _("[Link if you don't see image]({url})").format(url=url),
                    escape_formatting=False,
                ),
                image=url,
                footer=_("Requested by {req} • From r/{r}").format(
                    req=ctx.author.display_name, r=subr
                ),
            )
        elif url.startswith("https://gfycat.com"):
            em = (
                _("Here is {name} gif ... ")
                + emoji
                + _("\n\nRequested by {req} • From {r}\n{url}")
            ).format(name=name, req=bold(ctx.author.display_name), r=bold(subr), url=url)
        return em

    async def _make_embed_reddit_details(
        self, ctx: commands.Context, sub: str, name: str, emoji: str
    ):
        """Function to make the embed for all Reddit API images with details."""
        try:
            url, subr, author, title, post = await asyncio.wait_for(
                self._get_reddit_imgs_details(ctx, sub=sub), 3
            )
        except asyncio.TimeoutError:
            await ctx.send(
                "Failed to get an image.\n"
                "(Timeout error, it most likely means that Reddit API haven't returned images for 3 seconds)"
            )
            return
        if not url:
            return
        em = ""  # FIXME That thing is dumb.
        if url.endswith(GOOD_EXTENSIONS):
            em = await self._embed(
                color=await ctx.embed_colour(),
                title=(_("Here is {name} ... ") + emoji).format(name=name),
                description=(
                    _(
                        "**Reddit Author:** {author}\n**Title:** {title}\n"
                        "**[Link if you don't see image]({url})\n[Link of Reddit post]({post})**"
                    )
                ).format(author=author, title=title, url=url, post=post),
                image=url,
                footer=_("Requested by {req} • From r/{r}").format(
                    req=ctx.author.display_name, r=subr
                ),
            )
        elif url.startswith("https://gfycat.com"):
            em = (
                _("Here is {name} gif ... ")
                + emoji
                + _(
                    "\n{url}\n\n**Reddit Author:** {author}\n**Title:** {title}\n"
                    "Requested by {req} • From r/{r}\n**Link of Reddit post** {post}"
                )
            ).format(
                url=url,
                name=name,
                author=author,
                title=title,
                req=bold(ctx.author.display_name),
                r=bold(subr),
                post=post,
            )
        return em

    async def _make_embed_others_simple(
        self, ctx: commands.Context, name: str, emoji: str, url: str, img_arg: str, source: str
    ):
        """Function to make the embed for all others APIs images."""
        data = await self._get_others_imgs(ctx, facts=False, img_url=url)
        if not data:
            return
        em = await self._embed(
            color=await ctx.embed_colour(),
            title=(_("Here is {name} image ... ") + emoji).format(name=name),
            description=bold(
                _("[Link if you don't see image]({url})").format(url=data["img"][img_arg]),
                escape_formatting=False,
            ),
            image=data["img"][img_arg],
            footer=_("Requested by {req} • From {source}").format(
                req=ctx.author.display_name, source=source
            ),
        )
        return em

    async def _make_embed_others_facts(
        self,
        ctx: commands.Context,
        name: str,
        emoji: str,
        img_url: str,
        facts_url: str,
        fact_arg: str,
        img_arg: str,
        source: str,
    ):
        """Function to make the embed for all others APIs images."""
        data = await self._get_others_imgs(ctx, facts=True, img_url=img_url, facts_url=facts_url)
        if not data:
            return
        em = await self._embed(
            color=await ctx.embed_colour(),
            title=(_("Here is {name} ... ") + emoji).format(name=name),
            description=bold(
                _("{fact}\n[Link if you don't see image]({url})").format(
                    fact=data["fact"][fact_arg], url=data["img"][img_arg]
                ),
                escape_formatting=False,
            ),
            image=data["img"][img_arg],
            footer=_("Requested by {req} • From {source}").format(
                req=ctx.author.display_name, source=source
            ),
        )
        return em

    async def _maybe_embed(self, ctx: commands.Context, embed: Union[discord.Embed, str]):
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

    async def _send_reddit_msg(
        self, ctx: commands.Context, name: str, emoji: str, sub: list, details: bool = False
    ):
        """Main function called in all Reddit API commands."""
        async with ctx.typing():
            if details:
                embed = await self._make_embed_reddit_details(ctx, sub, name, emoji)
            else:
                embed = await self._make_embed_reddit_simple(ctx, sub, name, emoji)
        return await self._maybe_embed(ctx, embed)

    async def _send_other_msg(
        self,
        ctx: commands.Context,
        name: str,
        emoji: str,
        img_arg: str,
        source: str,
        facts: bool = False,
        img_url: str = None,
        facts_url: Optional[str] = None,
        facts_arg: Optional[str] = None,
    ):
        """Main function called in all others APIs commands."""
        async with ctx.typing():
            if facts:
                embed = await self._make_embed_others_facts(
                    ctx, name, emoji, img_url, facts_url, facts_arg, img_arg, source
                )
            else:
                embed = await self._make_embed_others_simple(
                    ctx, name, emoji, img_url, img_arg, source
                )
        return await self._maybe_embed(ctx, embed)

    @staticmethod
    async def _embed(
        color: Union[int, discord.Color] = None,
        title: str = None,
        description: str = None,
        image: str = None,
        footer: Optional[str] = None,
    ):
        em = discord.Embed(color=color, title=title, description=description)
        em.set_image(url=image)
        if footer:
            em.set_footer(text=footer)
        return em
