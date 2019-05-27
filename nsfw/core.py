import discord

import aiohttp
import json

from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import bold, box, inline

from random import choice
from typing import Optional

from .constants import (
    REDDIT_BASEURL,
    REDDIT_ENDPOINT,
    IMGUR_LINKS,
    GOOD_EXTENSIONS,
    NEKOBOT_BASEURL,
    Stuff,
)

_ = Translator("Nsfw", __file__)


@cog_i18n(_)
class Core(Stuff):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def _get_imgs(self, ctx, sub=None, url=None, subr=None):
        """Get images from Reddit API."""
        try:
            async with self.session.get(REDDIT_BASEURL + choice(sub) + REDDIT_ENDPOINT) as reddit:
                if reddit.status != 200:
                    return None, await self._api_errors_msg(ctx, error_code=reddit.status)
                try:
                    data = await reddit.json(content_type=None)
                    content = data[0]["data"]["children"][0]["data"]
                    url = content["url"]
                    subr = content["subreddit"]
                except (KeyError, ValueError, json.decoder.JSONDecodeError):
                    url, subr = await self._get_imgs(ctx, sub=sub, url=url, subr=subr)
                if url.startswith(IMGUR_LINKS):
                    url = url + ".png"
                elif url.endswith(".mp4"):
                    url = url[:-3] + "gif"
                elif url.endswith(".gifv"):
                    url = url[:-1]
                elif not url.endswith(GOOD_EXTENSIONS) and not url.startswith(
                    "https://gfycat.com"
                ):
                    url, subr = await self._get_imgs(ctx, sub=sub, url=url, subr=subr)
                return url, subr
        except aiohttp.client_exceptions.ClientConnectionError:
            await self._api_errors_msg(ctx, error_code="JSON decode failed")
            return None, None

    async def _get_imgs_others(self, ctx, api_category=None):
        """Get images from Nekobot API for hentai and porngif commands."""
        try:
            async with self.session.get(NEKOBOT_BASEURL + choice(api_category)) as others:
                if others.status != 200:
                    return None, await self._api_errors_msg(ctx, error_code=others.status)
                data = await others.json(content_type=None)
                url = data["message"]
                return url
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

    async def _nsfw_channel_check(self, ctx):
        """Message for non-nsfw channels."""
        if not ctx.message.channel.is_nsfw():
            embed = discord.Embed(
                title="\N{LOCK} " + _("You can't use that command in a non-NSFW channel !"),
                color=0xAA0000,
            )
        return embed

    async def _make_embed(self, ctx, sub, name, url):
        """Function to make the embed for all Reddit API images."""
        url, subr = await self._get_imgs(ctx, sub=sub, url=None, subr=None)
        if url is None:
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
                req=bold(f"{ctx.author.display_name}"),
                emoji=await self.emoji(),
                r=bold(f"r/{subr}"),
                url=url,
            )
        return em

    async def _make_embed_others(self, ctx, name, api_category):
        """Function to make embed for Nekobot API images."""
        url = await self._get_imgs_others(ctx, api_category=api_category)
        if url is None:
            return
        em = await self._embed(
            color=0x891193,
            title=(_("Here is {name} image ...") + " \N{EYES}").format(name=name),
            description=bold(_("[Link if you don't see image]({url})")).format(url=url),
            image=url,
            footer=_("Requested by {req} {emoji} • From Nekobot API").format(
                req=ctx.author.display_name, emoji=await self.emoji()
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
        except discord.errors.HTTPException:
            return

    async def _send_msg(self, ctx, name, sub=None):
        """Main function called in all Reddit API commands."""
        async with ctx.typing():
            if not ctx.guild or ctx.message.channel.is_nsfw():
                embed = await self._make_embed(ctx, sub, name, url=None)
        return await self._maybe_embed(
            ctx,
            embed=(
                await self._nsfw_channel_check(ctx)
                if (hasattr(ctx.channel, "is_nsfw") and (not (ctx.channel.is_nsfw())))
                else embed
            ),
        )

    async def _send_msg_others(self, ctx, name, api_category=None):
        """Main function called in all Nekobot API commands."""
        async with ctx.typing():
            if not ctx.guild or ctx.message.channel.is_nsfw():
                embed = await self._make_embed_others(ctx, name, api_category)
        return await self._maybe_embed(
            ctx,
            embed=(
                await self._nsfw_channel_check(ctx)
                if (hasattr(ctx.channel, "is_nsfw") and (not (ctx.channel.is_nsfw())))
                else embed
            ),
        )

    @staticmethod
    async def _embed(
        color=None, title=None, description=None, image=None, footer: Optional[str] = None
    ):
        em = discord.Embed(color=color, title=title, description=description)
        em.set_image(url=image)
        if footer:
            em.set_footer(text=footer)
        return em

    def cog_unload(self): 
        self.bot.loop.create_task(self.session.close())
