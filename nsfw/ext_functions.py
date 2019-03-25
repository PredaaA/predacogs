import discord

import aiohttp
import random

from redbot.core import commands

EMOJIS = random.choice(
    [
        "\N{AUBERGINE}",
        "\N{SMIRKING FACE}",
        "\N{PEACH}",
        "\N{SPLASHING SWEAT SYMBOL}",
        "\N{BANANA}",
        "\N{KISS MARK}",
    ]
)

BASE_URL = "https://api.reddit.com/r/"
ENDPOINT = "/random"

GOOD_EXTENSIONS = ".png", ".jpg", ".jpeg", ".gif"


class Functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def _get_imgs(self, ctx, sub=None, url=None, subr=None, text=None, cmd=None):
        sub = random.choice(sub)
        async with self.session.get(BASE_URL + f"{sub}" + ENDPOINT) as reddit:
            data = await reddit.json()
        try:
            url = data[0]["data"]["children"][0]["data"]["url"]
            subr = data[0]["data"]["children"][0]["data"]["subreddit"]
            text = data[0]["data"]["children"][0]["data"]["selftext"]
        except KeyError:
            await self._retry(ctx, cmd)
        return url, subr, text

    async def _retry(self, ctx, cmd):
        return await ctx.invoke(cmd)

    async def blocked_msg(self, ctx):
        em = discord.Embed(
            title="\N{LOCK} You can't use that command in a non-NSFW channel !", color=0xAA0000
        )
        return em

    async def _make_embed(self, ctx, subr, name, url):
        em = discord.Embed(
            color=0x891193,
            title="Here is {name} image ... \N{EYES}".format(name=name),
            description="[**Link if you don't see image**]({url})".format(url=url),
        )
        em.set_footer(
            text="Requested by {req} {emoji} • From r/{r}".format(
                req=ctx.author.display_name, emoji=EMOJIS, r=subr
            )
        )
        if url.endswith(GOOD_EXTENSIONS):
            em.set_image(url=url)
        if url.startswith("https://gfycat.com"):
            em = "Here is {name} gif ... \N{EYES}\n\nRequested by **{req}** {emoji} • From **r/{r}**\n{url}".format(
                name=name, req=ctx.author.display_name, emoji=EMOJIS, r=subr, url=url
            )

        return em

    async def _maybe_embed(self, ctx, embed):
        if type(embed) == discord.Embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed)
