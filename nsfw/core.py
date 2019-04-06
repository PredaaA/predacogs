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
                url, subr, text = await self._get_imgs(ctx, sub=sub, url=url, subr=subr)
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
                url, subr = await self._get_imgs(ctx, sub=sub, url=url, subr=subr)
        return url, subr

    async def _nsfw_channel_check(self, ctx, embed=None):
        if not ctx.message.channel.is_nsfw():
            embed = discord.Embed(
                title="\N{LOCK} You can't use that command in a non-NSFW channel !", color=0xAA0000
            )
        return embed

    async def _emojis(self):
        return random.choice(EMOJIS)

    emoji = _emojis

    async def _make_embed(self, ctx, sub, subr, name, url):
        url, subr = await self._get_imgs(ctx, sub=sub, url=None, subr=None)
        if url.endswith(GOOD_EXTENSIONS):
            em = await self._embed(
                ctx,
                color=0x891193,
                title="Here is {name} image ... \N{EYES}".format(name=name),
                description="[**Link if you don't see image**]({url})".format(url=url),
                image=url,
                text="Requested by {req} {emoji} • From r/{r}".format(
                    req=ctx.author.display_name, emoji=await self.emoji(), r=subr
                ),
            )
        if url.startswith("https://gfycat.com"):
            em = "Here is {name} gif ... \N{EYES}\n\nRequested by **{req}** {emoji} • From **r/{r}**\n{url}".format(
                name=name, req=ctx.author.display_name, emoji=await self.emoji(), r=subr, url=url
            )
        return em

    async def _make_embed_others(self, ctx, name, api_category=None):
        api = subs.NEKOBOT_BASEURL + random.choice(api_category)
        async with self.session.get(api) as i:
            data = await i.json(content_type=None)
            url = data["message"]
            embed = await self._embed(
                ctx,
                color=0x891193,
                title="Here is {name} image ... \N{EYES}".format(name=name),
                description="[**Link if you don't see image**]({url})".format(url=url),
                image=url,
                text="Requested by {req} {emoji} • From Nekobot API".format(
                    req=ctx.author.display_name, emoji=await self.emoji()
                ),
            )
            async with ctx.typing():
                if not ctx.guild or ctx.message.channel.is_nsfw():
                    embed = embed
            return await self._maybe_embed(
                ctx,
                embed=(
                    await self._nsfw_channel_check(ctx)
                    if (hasattr(ctx.channel, "is_nsfw") and (not (ctx.channel.is_nsfw())))
                    else embed
                ),
            )

    async def _maybe_embed(self, ctx, embed):
        if type(embed) == discord.Embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed)

    async def _send_msg(self, ctx, name, sub=None, subr=None):
        async with ctx.typing():
            if not ctx.guild or ctx.message.channel.is_nsfw():
                embed = await self._make_embed(ctx, sub, subr, name, url=None)
        return await self._maybe_embed(
            ctx,
            embed=(
                await self._nsfw_channel_check(ctx)
                if (hasattr(ctx.channel, "is_nsfw") and (not (ctx.channel.is_nsfw())))
                else embed
            ),
        )

    @staticmethod
    async def _embed(ctx, color=None, title=None, description=None, image=None, text=None):
        em = discord.Embed(color=color, title=title, description=description)
        em.set_image(url=image)
        em.set_footer(text=text)
        return em

    def __unload(self):
        self.bot.loop.create_task(self.session.close())
