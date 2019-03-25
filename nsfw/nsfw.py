import discord

from redbot.core import checks, commands

from . import subrs
from .ext_functions import Functions, EMOJIS

import aiohttp
import random


GOOD_EXTENSIONS = ".png", ".jpg", ".jpeg", ".gif"
IMGUR_LINKS = "http://imgur.com", "https://m.imgur.com", "https://imgur.com"


class Nsfw(Functions, commands.Cog):
    """Send random NSFW images from random subreddits"""

    __author__ = ["Predä", "aikaterna"]
    __version__ = "1.0.1"

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(name="4k", aliases=["4K"])
    async def four_k(self, ctx):
        """Show some 4k images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.FOUR_K, url=None, subr=None, text=None, cmd=self.four_k
            )
            # TODO : Create a function for not imgs and reconfigure links
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.four_k)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.AHEGAO, url=None, subr=None, text=None, cmd=self.ahegao
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.ahegao)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.ASS, url=None, subr=None, text=None, cmd=self.ass
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.ass)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.ANAL, url=None, subr=None, text=None, cmd=self.anal
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.anal)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.BDSM, url=None, subr=None, text=None, cmd=self.bdsm
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.bdsm)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.BLACKCOCK, url=None, subr=None, text=None, cmd=self.blackcock
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.blackcock)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.BLOWJOB, url=None, subr=None, text=None, cmd=self.blowjob
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.blowjob)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.BOOBS, url=None, subr=None, text=None, cmd=self.boobs
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.boobs)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.BOTTOMLESS, url=None, subr=None, text=None, cmd=self.bottomless
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.bottomless)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.CUNNI, url=None, subr=None, text=None, cmd=self.cunnilingus
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.cunnilingus)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.CUMSHOTS, url=None, subr=None, text=None, cmd=self.cumshot
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.cumshot)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.DEEPTHROAT, url=None, subr=None, text=None, cmd=self.deepthroat
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.deepthroat)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.DICK, url=None, subr=None, text=None, cmd=self.dick
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.dick)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.DOUBLE_P, url=None, subr=None, text=None, cmd=self.doublepenetration
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.doublepenetration)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.GAY_P, url=None, subr=None, text=None, cmd=self.gay
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.gay)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.GROUPS, url=None, subr=None, text=None, cmd=self.group
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.group)

            embed = await self._make_embed(ctx, subr, "group nudes", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def hentai(self, ctx):
        """Show some hentai images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.HENTAI, url=None, subr=None, text=None, cmd=self.hentai
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.hentai)

            embed = await self._make_embed(ctx, subr, "hentai", url)
            await self._maybe_embed(ctx, embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["hentaigifs"])
    async def hentaigif(self, ctx):
        """Show some hentai images from random subreddits."""
        try:
            if ctx.message.channel.is_nsfw() == False:
                em = await self.blocked_msg(ctx)
                return await ctx.send(embed=em)
        except:
            pass
        async with ctx.typing():
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.HENTAI_GIFS, url=None, subr=None, text=None, cmd=self.hentaigif
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.hentaigif)

            embed = await self._make_embed(ctx, subr, "hentai gif", url)
            await self._maybe_embed(ctx, embed=embed)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.LESBIANS, url=None, subr=None, text=None, cmd=self.lesbian
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.lesbian)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.MILF, url=None, subr=None, text=None, cmd=self.milf
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.milf)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.ORAL, url=None, subr=None, text=None, cmd=self.oral
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.oral)

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
            url = "https://nekobot.xyz/api/image?type=pgif"
            async with self.session.get(url) as i:
                data = await i.json()
                img = data["message"]
                em = discord.Embed(
                    color=0x891193,
                    title="Here is porn gif ... \N{EYES}",
                    description=f"[**Link if you don't see image**]({img})",
                )
                em.set_image(url=f"{img}")
                em.set_footer(
                    text="Requested by {name} {emoji}".format(
                        name=ctx.author.display_name, emoji=EMOJIS
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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.PUBLIC, url=None, subr=None, text=None, cmd=self.public
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.public)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.PUSSY, url=None, subr=None, text=None, cmd=self.pussy
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.pussy)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.REAL_GIRLS, url=None, subr=None, text=None, cmd=self.realgirls
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.realgirls)

            embed = await self._make_embed(ctx, subr, "real nudes", url)
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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.RULE_34, url=None, subr=None, text=None, cmd=self.rule34
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.rule34)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.THIGHS, url=None, subr=None, text=None, cmd=self.thigh
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.thigh)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.TRAPS, url=None, subr=None, text=None, cmd=self.trap
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.trap)

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
            url, subr, text = await self._get_imgs(
                ctx, sub=subrs.WILD, url=None, subr=None, text=None, cmd=self.wild
            )
            if url.startswith(IMGUR_LINKS):
                url = url + ".png"
            if url.endswith(".gifv"):
                url = url[:-1]
            if text or not url.endswith(GOOD_EXTENSIONS):
                return await ctx.invoke(self.wild)

            embed = await self._make_embed(ctx, subr, "gonewild", url)
            await self._maybe_embed(ctx, embed=embed)

    def __unload(self):
        self.bot.loop.create_task(self.session.close())
