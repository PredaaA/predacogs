import discord

import aiohttp
import random
import json

from .subs import EMOJIS
from . import subs

BASE_URL = "https://api.reddit.com/r/"
ENDPOINT = "/random"

IMGUR_LINKS = "http://imgur.com", "https://m.imgur.com", "https://imgur.com"
GOOD_EXTENSIONS = ".png", ".jpg", ".jpeg", ".gif"


class Functions:

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    # TODO: Use something different for getting images, like caching.
    # Or maybe not ? Works well now without ctx.invoke.
    async def _get_imgs(self, ctx, sub=None, url=None, subr=None):
        csub = random.choice(sub)
        async with self.session.get(BASE_URL + csub + ENDPOINT) as reddit:
            try:
                data = await reddit.json(content_type=None)
                content = data[0]["data"]["children"][0]["data"]
                url = content["url"]
                subr = content["subreddit"]
                text = content["selftext"]
            except (KeyError, ValueError, json.decoder.JSONDecodeError):
                url, subr, text = await self._get_imgs(ctx, sub=sub)
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".mp4"):
                url = url[:-3] + "gif"
            if url.endswith(".gifv"):
                url = url[:-1]
            if (
                text
                or not url.endswith(GOOD_EXTENSIONS)
                and not url.startswith("https://gfycat.com")
            ):
                url, subr = await self._get_imgs(ctx, sub=sub, url=url)
        return url, subr

    async def _nsfw_channel_check(self, ctx, embed=None):
        if ctx.message.channel.is_nsfw() == False:
            embed = discord.Embed(
                title="\N{LOCK} You can't use that command in a non-NSFW channel !", color=0xAA0000
            )
        return embed

    async def _emojis(self, emoji=None):
        emoji = random.choice(EMOJIS)
        return emoji

    async def _make_embed(self, ctx, subr, name, url):
        emoji = await self._emojis(emoji=None)
        em = discord.Embed(
            color=0x891193,
            title="Here is {name} image ... \N{EYES}".format(name=name),
            description="[**Link if you don't see image**]({url})".format(url=url),
        )
        em.set_footer(
            text="Requested by {req} {emoji} • From r/{r}".format(
                req=ctx.author.display_name, emoji=emoji, r=subr
            )
        )
        if url.endswith(GOOD_EXTENSIONS):
            em.set_image(url=url)
        if url.startswith("https://gfycat.com"):
            em = "Here is {name} gif ... \N{EYES}\n\nRequested by **{req}** {emoji} • From **r/{r}**\n{url}".format(
                name=name, req=ctx.author.display_name, emoji=emoji, r=subr, url=url
            )
        return em

    async def _make_embed_others(self, ctx, name, api_category=None):
        api = subs.NEKOBOT_BASEURL + random.choice(api_category)
        async with self.session.get(api) as i:
            data = await i.json(content_type=None)
            url = data["message"]
            emoji = await self._emojis(emoji=None)
            try:
                if ctx.message.channel.is_nsfw() == True:
                    em = discord.Embed(
                        color=0x891193,
                        title="Here is {name} image ... \N{EYES}".format(name=name),
                        description="[**Link if you don't see image**]({url})".format(url=url),
                    )
                    em.set_image(url=url)
                    em.set_footer(
                        text="Requested by {req} {emoji} • From Nekobot API".format(
                            req=ctx.author.display_name, emoji=emoji
                        )
                    )
                else:
                    em = await self._nsfw_channel_check(ctx)
            except AttributeError:
                em = discord.Embed(
                    color=0x891193,
                    title="Here is {name} image ... \N{EYES}".format(name=name),
                    description="[**Link if you don't see image**]({url})".format(url=url),
                )
                em.set_image(url=url)
                em.set_footer(
                    text="Requested by {req} {emoji} • From Nekobot API".format(
                        req=ctx.author.display_name, emoji=emoji
                    )
                )
            return await ctx.send(embed=em)

    async def _maybe_embed(self, ctx, embed):
        if type(embed) == discord.Embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed)

    async def _send_msg(self, ctx, name, sub=None, subr=None):
        async with ctx.typing():
            try:
                if ctx.message.channel.is_nsfw() == True:
                    url, subr = await self._get_imgs(ctx, sub=sub, url=None, subr=None)
                    embed = await self._make_embed(ctx, subr, name, url)
                else:
                    embed = await self._nsfw_channel_check(ctx)
            except AttributeError:
                url, subr = await self._get_imgs(ctx, sub=sub, url=None, subr=None)
                embed = await self._make_embed(ctx, subr, name, url)
        await self._maybe_embed(ctx, embed=embed)

    def __unload(self):
        self.bot.loop.create_task(self.session.close())
