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


class Core:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def _get_imgs(self, ctx, sub=None, url=None, subr=None):
        async with self.session.get(BASE_URL + random.choice(sub) + ENDPOINT) as reddit:
            try:
                data = await reddit.json(content_type=None)
                content = data[0]["data"]["children"][0]["data"]
                url = content["url"]
                subr = content["subreddit"]
                text = content["selftext"]
            except (KeyError, ValueError, json.decoder.JSONDecodeError):
                url, subr, text = await self._get_imgs(ctx, sub=sub, url=url)
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
        if not ctx.message.channel.is_nsfw():
            embed = discord.Embed(
                title="\N{LOCK} You can't use that command in a non-NSFW channel !", color=0xAA0000
            )
        return embed

    async def _emojis(self, emoji=None):
        emoji = random.choice(EMOJIS)
        return emoji

    async def _make_embed(self, ctx, subr, name, url):
        emoji = await self._emojis(emoji=None)
        if url.endswith(GOOD_EXTENSIONS):
            em = await self._embed(
                ctx,
                color=0x891193,
                title="Here is {name} image ... \N{EYES}".format(name=name),
                description="[**Link if you don't see image**]({url})".format(url=url),
                image=url,
                text="Requested by {req} {emoji} • From r/{r}".format(
                    req=ctx.author.display_name, emoji=emoji, r=subr
                ),
            )
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
            embed = await self._embed(
                ctx,
                color=0x891193,
                title="Here is {name} image ... \N{EYES}".format(name=name),
                description="[**Link if you don't see image**]({url})".format(url=url),
                image=url,
                text="Requested by {req} {emoji} • From Nekobot API".format(
                    req=ctx.author.display_name, emoji=emoji
                ),
            )
            async with ctx.typing():  # TODO: Shorten this.
                if ctx.guild:
                    if ctx.message.channel.is_nsfw():
                        em = embed
                    else:
                        em = await self._nsfw_channel_check(ctx)
                else:
                    em = embed
            return await ctx.send(embed=em)

    async def _maybe_embed(self, ctx, embed):
        if type(embed) == discord.Embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed)

    async def _send_msg(self, ctx, name, sub=None, subr=None):
        async with ctx.typing():  # TODO: Shorten this.
            if ctx.guild:
                if ctx.message.channel.is_nsfw():
                    url, subr = await self._get_imgs(ctx, sub=sub, url=None, subr=None)
                    embed = await self._make_embed(ctx, subr, name, url)
                else:
                    embed = await self._nsfw_channel_check(ctx)
            else:
                url, subr = await self._get_imgs(ctx, sub=sub, url=None, subr=None)
                embed = await self._make_embed(ctx, subr, name, url)
        await self._maybe_embed(ctx, embed=embed)

    @staticmethod
    async def _embed(ctx, color=None, title=None, description=None, image=None, text=None):
        em = discord.Embed(color=color, title=title, description=description)
        em.set_image(url=image)
        em.set_footer(text=text)
        return em

    def __unload(self):
        self.bot.loop.create_task(self.session.close())
