import discord

from redbot.core import checks, commands

from .ext_functions import Functions
from . import subs

import aiohttp
import random


GOOD_EXTENSIONS = ".png", ".jpg", ".jpeg", ".gif"
IMGUR_LINKS = "http://imgur.com", "https://m.imgur.com", "https://imgur.com"


class Nsfw(Functions, commands.Cog):
    """Send random NSFW images from random subreddits"""

    __author__ = ["Predä", "aikaterna"]
    __version__ = "1.1"

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(name="4k", aliases=["4K"])
    async def four_k(self, ctx):
        """Show some 4k images from random subreddits."""
        # TODO : Make a function for that.
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.FOUR_K, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "4k", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def ahegao(self, ctx):
        """Show some ahegao images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.AHEGAO, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "ahegao", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["butt"])
    async def ass(self, ctx):
        """Show some ass images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.ASS, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "ass", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def anal(self, ctx):
        """Show some anal images/gifs from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.ANAL, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "anal", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def bdsm(self, ctx):
        """Show some bdsm from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.BDSM, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "bdsm", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["blackdick", "bcock", "bdick", "blackcocks", "blackdicks"])
    async def blackcock(self, ctx):
        """Show some blackcock images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.BLACKCOCK, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "blackcock", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["blowjobs", "blowj", "bjob"])
    async def blowjob(self, ctx):
        """Show some blowjob images/gifs from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.BLOWJOB, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "blowjob", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["boob", "tits", "titties"])
    async def boobs(self, ctx):
        """Show some boobs images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.BOOBS, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "boobs", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["boless"])
    async def bottomless(self, ctx):
        """Show some bottomless images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.BOTTOMLESS, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "bottomless", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["cunni"])
    async def cunnilingus(self, ctx):
        """Show some cunnilingus images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.CUNNI, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "cunnilingus", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["cum", "cumshots"])
    async def cumshot(self, ctx):
        """Show some cumshot images/gifs from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.CUMSHOTS, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "cumshot", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["deept"])
    async def deepthroat(self, ctx):
        """Show some deepthroat images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.DEEPTHROAT, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "deepthroat", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def dick(self, ctx):
        """Show some dicks images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.DICK, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "dick", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["doublep", "dpenetration", "doublepene"])
    async def doublepenetration(self, ctx):
        """Show some double penetration images/gifs from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.DOUBLE_P, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "double penetration", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["nudeman"])
    async def gay(self, ctx):
        """Show some gay porn from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.GAY_P, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "gay porn", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["groups"])
    async def group(self, ctx):
        """Show some groups nudes from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.GROUPS, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "group nudes", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["hentaigif"])
    async def hentai(self, ctx):
        """Show some hentai images/gifs from Nekobot API."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url = subs.NEKOBOT_BASEURL + random.choice(["hentai_anal", "hentai"])
            emoji = await self.emojis(emoji=None)
            async with self.session.get(url) as i:
                data = await i.json()
                img = data["message"]
                em = discord.Embed(
                    color=0x891193,
                    title="Here is hentai ... \N{EYES}",
                    description=f"[**Link if you don't see image**]({img})",
                )
                em.set_image(url=img)
                em.set_footer(
                    text="Requested by {name} {emoji} • From Nekobot API".format(
                        name=ctx.author.display_name, emoji=emoji
                    )
                )
        await ctx.send(embed=em)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def lesbian(self, ctx):
        """Show some lesbian gifs or images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.LESBIANS, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "lesbian", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["milfs"])
    async def milf(self, ctx):
        """Show some milf images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.MILF, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "milf", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["suck"])
    async def oral(self, ctx):
        """Show some oral gifs or images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.ORAL, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "oral", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["pgif"])
    async def porngif(self, ctx):
        """Show some porn gifs from Nekobot API."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url = subs.NEKOBOT_BASEURL + "pgif"
            emoji = await self.emojis(emoji=None)
            async with self.session.get(url) as i:
                data = await i.json()
                img = data["message"]
                em = discord.Embed(
                    color=0x891193,
                    title="Here is porn gif ... \N{EYES}",
                    description=f"[**Link if you don't see image**]({img})",
                )
                em.set_image(url=img)
                em.set_footer(
                    text="Requested by {name} {emoji} • From Nekobot API".format(
                        name=ctx.author.display_name, emoji=emoji
                    )
                )
        await ctx.send(embed=em)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def public(self, ctx):
        """Show some public nude images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.PUBLIC, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "public nudes", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def pussy(self, ctx):
        """Show some pussy nude images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.PUSSY, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "pussy", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def realgirls(self, ctx):
        """Show some real girls images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.REAL_GIRLS, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "real nudes", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["redheads", "ginger", "gingers"])
    async def redhead(self, ctx):
        """Show some red heads images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.REDHEADS, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "red head", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["r34"])
    async def rule34(self, ctx):
        """Show some rule34 images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.RULE_34, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "rule34", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["thighs"])
    async def thigh(self, ctx):
        """Show some thighs images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.THIGHS, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "thigh", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["traps", "trans", "girldick", "girldicks", "shemale", "shemales"])
    async def trap(self, ctx):
        """Show some traps from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.TRAPS, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "trap", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["gonewild", "gwild"])
    async def wild(self, ctx):
        """Show some gonewild images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr = await self._get_imgs(ctx, sub=subs.WILD, url=None, subr=None)
            embed = await self._make_embed(ctx, subr, "gonewild", url)
            await self._maybe_embed(ctx, embed=embed)

    def __unload(self):
        self.bot.loop.create_task(self.session.close())
