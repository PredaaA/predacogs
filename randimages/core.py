import discord

import aiohttp
import json

from redbot.core import Config
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import bold, box, inline

from random import choice
from typing import Optional

from .constants import REDDIT_BASEURL, IMGUR_LINKS, GOOD_EXTENSIONS

_ = Translator("Image", __file__)


@cog_i18n(_)
class Core:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    async def _get_reddit_imgs_simple(self, ctx, sub=None):
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

    async def _get_reddit_imgs_details(self, ctx, sub=None):
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
                    author, title, url, subr, nsfw, text = await self._get_reddit_imgs_details(
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
                    author, title, url, subr, nsfw = await self._get_reddit_imgs_details(ctx, sub=sub)
            return url, subr, author, title, post
        except aiohttp.client_exceptions.ClientConnectionError:
            await self._api_errors_msg(ctx, error_code="JSON decode failed")
            return None, None, None, None, None

    async def _get_others_imgs(self, ctx, facts: bool, img_url=None, facts_url=Optional[str]):
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

    async def _api_errors_msg(self, ctx, error_code=None):
        """Error message when API calls fail."""
        return await ctx.send(
            _("Error when trying to contact image service, please try again later. ")
            + "(Code: {})".format(inline(str(error_code)))
        )

    async def _nsfw_channel_check(self, ctx):
        """Message for non-nsfw channels."""
        if not ctx.message.channel.is_nsfw():
            em = discord.Embed(
                title="\N{LOCK} " + _("NSFW content in the link. Blocked in non-NSFW channel."),
                color=0xAA0000,
            )
        return em

    async def _make_embed_reddit_simple(self, ctx, sub, name, emoji, url):
        """Function to make the embed for all Reddit API images."""
        url, subr = await self._get_reddit_imgs_simple(ctx, sub=sub)
        if not url:
            return
        if url.endswith(GOOD_EXTENSIONS):
            em = await self._embed(
                color=await ctx.embed_colour(),
                title=(_("Here is {name} ... ") + emoji).format(name=name),
                description=bold(_("[Link if you don't see image]({url})")).format(url=url),
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

    async def _make_embed_reddit_details(self, ctx, sub, name, emoji, url):
        """Function to make the embed for all Reddit API images with details."""
        url, subr, author, title, post = await self._get_reddit_imgs_details(ctx, sub=sub)
        if not url:
            return
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

    async def _make_embed_others_simple(self, ctx, name, emoji, url, img_arg, source):
        """Function to make the embed for all others APIs images."""
        data = await self._get_others_imgs(ctx, facts=False, img_url=url)
        if not data:
            return
        em = await self._embed(
            color=await ctx.embed_colour(),
            title=(_("Here is {name} image ... ") + emoji).format(name=name),
            description=bold(_("[Link if you don't see image]({url})")).format(
                url=data["img"][img_arg]
            ),
            image=data["img"][img_arg],
            footer=_("Requested by {req} • From {source}").format(
                req=ctx.author.display_name, source=source
            ),
        )
        return em

    async def _make_embed_others_facts(
        self, ctx, name, emoji, img_url, facts_url, fact_arg, img_arg, source
    ):
        """Function to make the embed for all others APIs images."""
        data = await self._get_others_imgs(ctx, facts=True, img_url=img_url, facts_url=facts_url)
        if not data:
            return
        em = await self._embed(
            color=await ctx.embed_colour(),
            title=(_("Here is {name} ... ") + emoji).format(name=name),
            description=bold(_("{fact}\n[Link if you don't see image]({url})")).format(
                fact=data["fact"][fact_arg], url=data["img"][img_arg]
            ),
            image=data["img"][img_arg],
            footer=_("Requested by {req} • From {source}").format(
                req=ctx.author.display_name, source=source
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

    async def _send_reddit_msg(self, ctx, name, emoji, details: bool = False, sub=None):
        """Main function called in all Reddit API commands."""
        async with ctx.typing():
            if details:
                embed = await self._make_embed_reddit_details(ctx, sub, name, emoji, url=None)
            else:
                embed = await self._make_embed_reddit_simple(ctx, sub, name, emoji, url=None)
        return await self._maybe_embed(ctx, embed)

    async def _send_other_msg(
        self,
        ctx,
        name,
        emoji,
        img_arg,
        source,
        facts: bool = False,
        img_url=None,
        facts_url=Optional[str],
        facts_arg=Optional[str],
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
        color=None, title=None, description=None, image=None, footer: Optional[str] = None
    ):
        em = discord.Embed(color=color, title=title, description=description)
        em.set_image(url=image)
        if footer:
            em.set_footer(text=footer)
        return em
