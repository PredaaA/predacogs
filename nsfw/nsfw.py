import discord

from redbot.core import checks, commands
from redbot.core.i18n import Translator, cog_i18n

from .core import Core
from . import subs

_ = Translator("Nsfw", __file__)


@cog_i18n(_)
class Nsfw(Core, commands.Cog):
    """Send random NSFW images from random subreddits"""

    __author__ = ["Predä", "aikaterna"]
    __version__ = "1.9.6"

    @commands.command()
    async def nsfwversion(self, ctx):
        """Get the version of the installed Nsfw cog."""

        await self._version_msg(ctx, self.__version__)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(name="4k", aliases=["4K", "fourk"])
    async def four_k(self, ctx):
        """Show some 4k images from random subreddits."""

        await self._send_msg(ctx, _("4k"), sub=subs.FOUR_K, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["oface", "ofaces"])
    async def ahegao(self, ctx):
        """Show some ahegao images from random subreddits."""

        await self._send_msg(ctx, _("ahegao"), sub=subs.AHEGAO, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["butt", "booty"])
    async def ass(self, ctx):
        """Show some ass images from random subreddits."""

        await self._send_msg(ctx, _("ass"), sub=subs.ASS, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["sodomy"])
    async def anal(self, ctx):
        """Show some anal images/gifs from random subreddits."""

        await self._send_msg(ctx, _("anal"), sub=subs.ANAL, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["shibari"])
    async def bdsm(self, ctx):
        """Show some bdsm from random subreddits."""

        await self._send_msg(ctx, _("bdsm"), sub=subs.BDSM, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["blackdick", "bcock", "bdick", "blackcocks", "blackdicks"])
    async def blackcock(self, ctx):
        """Show some blackcock images from random subreddits."""

        await self._send_msg(ctx, _("black cock"), sub=subs.BLACKCOCK, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["blowjobs", "blowj", "bjob", "fellatio", "fellation"])
    async def blowjob(self, ctx):
        """Show some blowjob images/gifs from random subreddits."""

        await self._send_msg(ctx, _("blowjob"), sub=subs.BLOWJOB, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["boob", "boobies", "tits", "titties", "breasts", "breast"])
    async def boobs(self, ctx):
        """Show some boobs images from random subreddits."""

        await self._send_msg(ctx, _("boobs"), sub=subs.BOOBS, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["boless", "b_less"])
    async def bottomless(self, ctx):
        """Show some bottomless images from random subreddits."""

        await self._send_msg(ctx, _("bottomless"), sub=subs.BOTTOMLESS, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["cunni", "pussyeating"])
    async def cunnilingus(self, ctx):
        """Show some cunnilingus images from random subreddits."""

        await self._send_msg(ctx, _("cunnilingus"), sub=subs.CUNNI, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["cum", "cums", "cumshots"])
    async def cumshot(self, ctx):
        """Show some cumshot images/gifs from random subreddits."""

        await self._send_msg(ctx, _("cumshot"), sub=subs.CUMSHOTS, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["deept", "deepthroating"])
    async def deepthroat(self, ctx):
        """Show some deepthroat images from random subreddits."""

        await self._send_msg(ctx, _("deepthroat"), sub=subs.DEEPTHROAT, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["cock"])
    async def dick(self, ctx):
        """Show some dicks images from random subreddits."""

        await self._send_msg(ctx, _("dick"), sub=subs.DICK, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["doublep", "dpenetration", "doublepene", "doublepen"])
    async def doublepenetration(self, ctx):
        """Show some double penetration images/gifs from random subreddits."""

        await self._send_msg(ctx, _("double penetration"), sub=subs.DOUBLE_P, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["gpp"])
    async def gay(self, ctx):
        """Show some gay porn from random subreddits."""

        await self._send_msg(ctx, _("gay porn"), sub=subs.GAY_P, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["groups", "nudegroup", "nudegroups"])
    async def group(self, ctx):
        """Show some groups nudes from random subreddits."""

        await self._send_msg(ctx, "groups nudes", sub=subs.GROUPS, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["hentaigif"])
    async def hentai(self, ctx):
        """Show some hentai images/gifs from Nekobot API."""

        await self._send_msg_others(ctx, _("hentai"), api_category=["hentai_anal", "hentai"])

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["lesbians"])
    async def lesbian(self, ctx):
        """Show some lesbian gifs or images from random subreddits."""

        await self._send_msg(ctx, _("lesbian"), sub=subs.LESBIANS, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["milfs"])
    async def milf(self, ctx):
        """Show some milf images from random subreddits."""

        await self._send_msg(ctx, _("milf"), sub=subs.MILF, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["oralsex"])
    async def oral(self, ctx):
        """Show some oral gifs or images from random subreddits."""

        await self._send_msg(ctx, _("oral"), sub=subs.ORAL, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["pgif", "prongif"])
    async def porngif(self, ctx):
        """Show some porn gifs from Nekobot API."""

        await self._send_msg_others(ctx, _("porn gif"), api_category=["pgif"])

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["flashinggirl"])
    async def public(self, ctx):
        """Show some public nude images from random subreddits."""

        await self._send_msg(ctx, _("public nude"), sub=subs.PUBLIC, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["vagina", "puss"])
    async def pussy(self, ctx):
        """Show some pussy nude images from random subreddits."""

        await self._send_msg(ctx, _("pussy"), sub=subs.PUSSY, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def realgirls(self, ctx):
        """Show some real girls images from random subreddits."""

        await self._send_msg(ctx, _("real nudes"), sub=subs.REAL_GIRLS, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["redheads", "ginger", "gingers"])
    async def redhead(self, ctx):
        """Show some red heads images from random subreddits."""

        await self._send_msg(ctx, _("red head"), sub=subs.REDHEADS, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["r34"])
    async def rule34(self, ctx):
        """Show some rule34 images from random subreddits."""

        await self._send_msg(ctx, _("rule34"), sub=subs.RULE_34, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["thighs", "legs"])
    async def thigh(self, ctx):
        """Show some thighs images from random subreddits."""

        await self._send_msg(ctx, _("thigh"), sub=subs.THIGHS, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["traps", "trans", "girldick", "girldicks", "shemale", "shemales"])
    async def trap(self, ctx):
        """Show some traps from random subreddits."""

        await self._send_msg(ctx, _("trap"), sub=subs.TRAPS, subr=None)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["wild", "gwild"])
    async def gonewild(self, ctx):
        """Show some gonewild images from random subreddits."""

        await self._send_msg(ctx, _("gonewild"), sub=subs.WILD, subr=None)
