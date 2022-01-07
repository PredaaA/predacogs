import discord

from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n

import contextlib

from . import constants as sub
from .core import Core

_ = Translator("Nsfw", __file__)


@cog_i18n(_)
class Nsfw(Core):
    """
    Send random NSFW images from random subreddits

    If `[p]help Nsfw` or any other Nsfw commands are used in a non-nsfw channel,
    you will not be able to see the list of commands for this category.
    """

    @commands.command()
    async def nsfwversion(self, ctx: commands.Context):
        """Get the version of the installed Nsfw cog."""

        await self._version_msg(ctx, self.__version__, self.__author__)

    @commands.is_owner()
    @commands.group()
    async def nsfwset(self, ctx: commands.Context):
        """Settings for the Nsfw cog."""

    @nsfwset.command()
    async def switchredditapi(self, ctx: commands.Context):
        """Toggle to use Reddit API directly with the cost of getting ratelimited fast, or use Martine API with faster results and no ratelimits problems.

        Defaults to Martine API."""
        val = await self.config.use_reddit_api()
        await self.config.use_reddit_api.set(not val)
        await ctx.send(
            "Switched to Reddit API. Warning: Your bot might be ratelimited by Reddit fast."
            if not val
            else "Switched back to Martine API."
        )

    @commands.is_nsfw()
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cleandm(self, ctx: commands.Context, number: int):
        """
        Delete a number specified of DM's from the bot.

        `<number>`: Number of messages from the bot you want
        to delete in your DM's.
        """
        if ctx.guild:
            return await ctx.send(_("This command works only for DM's messages !"))
        async for message in ctx.channel.history(limit=number):
            if message.author.id == ctx.bot.user.id:
                with contextlib.suppress(discord.NotFound):
                    await message.delete()
        await ctx.tick()

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(name="4k", aliases=["4K", "fourk"])
    async def four_k(self, ctx: commands.Context):
        """Sends some 4k images from random subreddits."""

        await self._send_msg(ctx, _("4k"), sub.FOUR_K)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["oface", "ofaces"])
    async def ahegao(self, ctx: commands.Context):
        """Sends some ahegao images from random subreddits."""

        await self._send_msg(ctx, _("ahegao"), sub.AHEGAO)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["butt", "booty"])
    async def ass(self, ctx: commands.Context):
        """Sends some ass images from random subreddits."""

        await self._send_msg(ctx, _("ass"), sub.ASS)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["asian"])
    async def asianporn(self, ctx: commands.Context):
        """Sends some asian porn images."""

        await self._send_msg(ctx, _("asian porn"), sub.ASIANPORN)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["sodomy"])
    async def anal(self, ctx: commands.Context):
        """Sends some anal images/gifs from random subreddits."""

        await self._send_msg(ctx, _("anal"), sub.ANAL)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def bbw(self, ctx: commands.Context):
        """Sends some bbw images."""

        await self._send_msg(ctx, _("bbw"), sub.BBW)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["shibari"])
    async def bdsm(self, ctx: commands.Context):
        """Sends some bdsm from random subreddits."""

        await self._send_msg(ctx, _("bdsm"), sub.BDSM)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["blackdick", "bcock", "bdick", "blackcocks", "blackdicks"])
    async def blackcock(self, ctx: commands.Context):
        """Sends some blackcock images from random subreddits."""

        await self._send_msg(ctx, _("black cock"), sub.BLACKCOCK)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["blowjobs", "blowj", "bjob", "fellatio", "fellation"])
    async def blowjob(self, ctx: commands.Context):
        """Sends some blowjob images/gifs from random subreddits."""

        await self._send_msg(ctx, _("blowjob"), sub.BLOWJOB)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["boob", "boobies", "tits", "titties", "breasts", "breast"])
    async def boobs(self, ctx: commands.Context):
        """Sends some boobs images from random subreddits."""

        await self._send_msg(ctx, _("boobs"), sub.BOOBS)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["boless"])
    async def bottomless(self, ctx: commands.Context):
        """Sends some bottomless images from random subreddits."""

        await self._send_msg(ctx, _("bottomless"), sub.BOTTOMLESS)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def cosplay(self, ctx: commands.Context):
        """Sends some nsfw cosplay images from random subreddits."""

        await self._send_msg(ctx, _("nsfw cosplay"), sub.COSPLAY)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["cunni", "pussyeating"])
    async def cunnilingus(self, ctx: commands.Context):
        """Sends some cunnilingus images from random subreddits."""

        await self._send_msg(ctx, _("cunnilingus"), sub.CUNNI)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["cum", "cums", "cumshots"])
    async def cumshot(self, ctx: commands.Context):
        """Sends some cumshot images/gifs from random subreddits."""

        await self._send_msg(ctx, _("cumshot"), sub.CUMSHOTS)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["deept", "deepthroating"])
    async def deepthroat(self, ctx: commands.Context):
        """Sends some deepthroat images from random subreddits."""

        await self._send_msg(ctx, _("deepthroat"), sub.DEEPTHROAT)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["cock"])
    async def dick(self, ctx: commands.Context):
        """Sends some dicks images from random subreddits."""

        await self._send_msg(ctx, _("dick"), sub.DICK)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["doublep"])
    async def doublepenetration(self, ctx: commands.Context):
        """Sends some double penetration images/gifs from random subreddits."""

        await self._send_msg(ctx, _("double penetration"), sub.DOUBLE_P)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def ebony(self, ctx: commands.Context):
        """Sends some ebony images."""

        await self._send_msg(ctx, _("ebony"), sub.EBONY)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["facial"])
    async def facials(self, ctx: commands.Context):
        """Sends some facials images from random subreddits."""

        await self._send_msg(ctx, _("facials"), sub.FACIALS)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["feets", "feetish"])
    async def feet(self, ctx: commands.Context):
        """Sends some feet images from random subreddits."""

        await self._send_msg(ctx, _("feets"), sub.FEET)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def femdom(self, ctx: commands.Context):
        """Sends some femdom images from random subreddits."""

        await self._send_msg(ctx, _("femdom"), sub.FEMDOM)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["futanari"])
    async def futa(self, ctx: commands.Context):
        """Sends some futa images from random subreddits."""

        await self._send_msg(ctx, _("futa"), sub.FUTA)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["gayporn"])
    async def gay(self, ctx: commands.Context):
        """Sends some gay porn from random subreddits."""

        await self._send_msg(ctx, _("gay porn"), sub.GAY_P)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["groups", "nudegroup", "nudegroups"])
    async def group(self, ctx: commands.Context):
        """Sends some groups nudes from random subreddits."""

        await self._send_msg(ctx, "groups nudes", sub.GROUPS)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def hentai(self, ctx: commands.Context):
        """Sends some hentai images/gifs from Nekobot API."""

        await self._send_other_msg(
            ctx,
            name=_("hentai"),
            arg="message",
            source="Nekobot API",
            url=sub.NEKOBOT_URL.format(sub.NEKOBOT_HENTAI),
        )

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["lesbians"])
    async def lesbian(self, ctx: commands.Context):
        """Sends some lesbian gifs or images from random subreddits."""

        await self._send_msg(ctx, _("lesbian"), sub.LESBIANS)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["milfs"])
    async def milf(self, ctx: commands.Context):
        """Sends some milf images from random subreddits."""

        await self._send_msg(ctx, _("milf"), sub.MILF)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["oralsex"])
    async def oral(self, ctx: commands.Context):
        """Sends some oral gifs or images from random subreddits."""

        await self._send_msg(ctx, _("oral"), sub.ORAL)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["pgif", "prongif"])
    async def porngif(self, ctx: commands.Context):
        """Sends some porn gifs from Nekobot API."""

        await self._send_other_msg(
            ctx,
            name=_("porn gif"),
            arg="message",
            source="Nekobot API",
            url=sub.NEKOBOT_URL.format("pgif"),
        )

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def public(self, ctx: commands.Context):
        """Sends some public nude images from random subreddits."""

        await self._send_msg(ctx, _("public nude"), sub.PUBLIC)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["vagina", "puss"])
    async def pussy(self, ctx: commands.Context):
        """Sends some pussy nude images from random subreddits."""

        await self._send_msg(ctx, _("pussy"), sub.PUSSY)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command()
    async def realgirls(self, ctx: commands.Context):
        """Sends some real girls images from random subreddits."""

        await self._send_msg(ctx, _("real nudes"), sub.REAL_GIRLS)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["redheads", "ginger", "gingers"])
    async def redhead(self, ctx: commands.Context):
        """Sends some red heads images from random subreddits."""

        await self._send_msg(ctx, _("red head"), sub.REDHEADS)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["r34"])
    async def rule34(self, ctx: commands.Context):
        """Sends some rule34 images from random subreddits."""

        await self._send_msg(ctx, _("rule34"), sub.RULE_34)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["squirts"])
    async def squirt(self, ctx: commands.Context):
        """Sends some squirts images from random subreddits."""

        await self._send_msg(ctx, _("squirt"), sub.SQUIRTS)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["thighs", "legs"])
    async def thigh(self, ctx: commands.Context):
        """Sends some thighs images from random subreddits."""

        await self._send_msg(ctx, _("thigh"), sub.THIGHS)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["groupsex"])
    async def threesome(self, ctx: commands.Context):
        """Sends some threesome images."""

        await self._send_msg(ctx, _("threesome"), sub.THREESOME)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["trap", "shemale", "shemales"])
    async def trans(self, ctx: commands.Context):
        """Sends some trans from random subreddits."""

        await self._send_msg(ctx, _("trans"), sub.TRANS)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["wild", "gwild"])
    async def gonewild(self, ctx: commands.Context):
        """Sends some gonewild images from random subreddits."""

        await self._send_msg(ctx, _("gonewild"), sub.WILD)

    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.command(aliases=["yiffs"])
    async def yiff(self, ctx: commands.Context):
        """Sends some yiff images from random subreddits."""

        await self._send_msg(ctx, _("yiff"), sub.YIFF)
