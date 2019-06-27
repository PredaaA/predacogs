from redbot.core import checks, commands
from redbot.core.i18n import Translator, cog_i18n

from .core import Core
from . import constants as sub


_ = Translator("Image", __file__)


@cog_i18n(_)
class RandImages(Core, commands.Cog):
    """Send random images (animals, art ...) from different APIs."""

    __author__ = "Predä"
    __version__ = "1.0"

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def art(self, ctx):
        """Send art from random subreddits."""

        await self._send_reddit_msg(
            ctx, name=_("art image"), emoji="\N{ARTIST PALETTE}", sub=sub.ART, details=True
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def birb(self, ctx):
        """Send a random birb image from alexflipnote API."""

        await self._send_other_msg(
            ctx,
            name=_("birb"),
            emoji="\N{BIRD}",
            source="alexflipnote API",
            img_url="https://api.alexflipnote.xyz/birb",
            img_arg="file",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["cats"])
    async def cat(self, ctx):
        """Send a random cat image some-random-api.ml API."""

        await self._send_other_msg(
            ctx,
            name=_("cat"),
            emoji="\N{CAT FACE}",
            source="nekos.life",
            img_url="https://nekos.life/api/v2/img/meow",
            img_arg="url",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["catsfact"])
    async def catfact(self, ctx):
        """Send a random cat fact with a random cat image from some-random-api.ml API."""

        await self._send_other_msg(
            ctx,
            name=_("a cat fact with a random cat image"),
            emoji="\N{CAT FACE}",
            source="nekos.life",
            img_url="https://nekos.life/api/v2/img/meow",
            img_arg="url",
            facts_url="https://some-random-api.ml/facts/cat",
            facts_arg="fact",
            facts=True,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def coffee(self, ctx):
        """Send a random coffee image from alexflipnote API."""

        await self._send_other_msg(
            ctx,
            name=_("your coffee"),
            emoji="\N{HOT BEVERAGE}",
            source="alexflipnote API",
            img_url="https://coffee.alexflipnote.xyz/random.json",
            img_arg="file",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["cuteness"])
    async def cute(self, ctx):
        """Send a random cute images from random subreddits."""

        await self._send_reddit_msg(
            ctx, name=_("a cute image"), emoji="❤️", sub=sub.CUTE, details=False
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["dogs"])
    async def dog(self, ctx):
        """Send a random dog image from random.dog API."""

        await self._send_other_msg(
            ctx,
            name=_("dog"),
            emoji="\N{DOG FACE}",
            source="random.dog",
            img_url="https://random.dog/woof.json",
            img_arg="url",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["dogsfact"])
    async def dogfact(self, ctx):
        """Send a random dog fact with a random dog image from some-random-api.ml API."""

        await self._send_other_msg(
            ctx,
            name=_("a dog fact with a random dog image"),
            emoji="\N{DOG FACE}",
            source="random.dog",
            img_url="https://random.dog/woof.json",
            img_arg="url",
            facts_url="https://some-random-api.ml/facts/dog",
            facts_arg="fact",
            facts=True,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def duck(self, ctx):
        """Send a random fox image from random-d.uk API"""

        await self._send_other_msg(
            ctx,
            name=_("duck"),
            emoji="\N{DUCK}",
            source="random-d.uk",
            img_url="https://random-d.uk/api/v1/random",
            img_arg="url",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["ferrets"])
    async def ferret(self, ctx):
        """Send a random ferrets images from random subreddits."""

        await self._send_reddit_msg(
            ctx, name=_("a ferret image"), emoji="❤️", sub=sub.FERRETS, details=False
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["foxes"])
    async def fox(self, ctx):
        """Send a random fox image from randomfox.ca API"""

        await self._send_other_msg(
            ctx,
            name=_("fox"),
            emoji="\N{FOX FACE}",
            source="randomfox.ca",
            img_url="https://randomfox.ca/floof",
            img_arg="image",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["pandas"])
    async def panda(self, ctx):
        """Send a random panda image from some-random-api.ml API."""

        await self._send_other_msg(
            ctx,
            name=_("panda"),
            emoji="\N{PANDA FACE}",
            source="some-random-api.ml",
            img_url="https://some-random-api.ml/pandaimg",
            img_arg="link",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def lizard(self, ctx):
        """Send a random lizard image from nekos.life API"""

        await self._send_other_msg(
            ctx,
            name=_("lizard"),
            emoji="\N{LIZARD}",
            source="nekos.life",
            img_url="https://nekos.life/api/lizard",
            img_arg="url",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["memes"])
    async def meme(self, ctx):
        """Send a random dank meme from random subreddits."""

        await self._send_reddit_msg(
            ctx, name=_("meme image"), emoji="\N{OK HAND SIGN}", sub=sub.MEMES, details=False
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["pandasfact"])
    async def pandafact(self, ctx):
        """Send a random panda fact with a random panda image from some-random-api.ml API."""

        await self._send_other_msg(
            ctx,
            name=_("a panda fact with a random panda image"),
            emoji="\N{PANDA FACE}",
            source="some-random-api.ml",
            img_url="https://some-random-api.ml/pandaimg",
            img_arg="link",
            facts_url="https://some-random-api.ml/facts/panda",
            facts_arg="fact",
            facts=True,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["pikachu"])
    async def pika(self, ctx):
        """Send a random Pikachu image or GIF from some-random-api.ml API."""

        await self._send_other_msg(
            ctx,
            name=_("Pikachu"),
            emoji="❤️",
            source="some-random-api.ml",
            img_url="https://some-random-api.ml/pikachuimg",
            img_arg="link",
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def shiba(self, ctx):
        """Send a random shiba image from shiba.online API."""

        await self._send_other_msg(
            ctx,
            name=_("shiba"),
            emoji="\N{DOG FACE}",
            source="shibe.online",
            img_url="http://shibe.online/api/shibes",
            img_arg=0,
            facts=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["photography"])
    async def photo(self, ctx):
        """Send a random photography from random subreddits."""

        await self._send_reddit_msg(
            ctx,
            name=_("a photography"),
            emoji="\N{CAMERA WITH FLASH}",
            sub=sub.PHOTOS,
            details=True,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["subr"])
    async def subreddit(self, ctx, *, subreddit):
        """Send a random image from that chosen subreddit."""

        await self._send_reddit_msg(
            ctx,
            name=_("random image"),
            emoji="\N{FRAME WITH PICTURE}",
            sub=[str(subreddit)],
            details=False,
        )

    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["wallp"])
    async def wallpaper(self, ctx):
        """Send a random wallpaper image from random subreddits."""

        await self._send_reddit_msg(
            ctx,
            name=_("a wallpaper"),
            emoji="\N{FRAME WITH PICTURE}",
            sub=sub.WALLPAPERS,
            details=True,
        )
