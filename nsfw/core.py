import asyncio
import json
import sys
from random import choice
from typing import List, Optional, Union

import aiohttp
import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import bold, box, inline

from .constants import GOOD_EXTENSIONS, IMGUR_LINKS, MARTINE_API_BASE_URL, REDDIT_BASEURL, emoji

_ = Translator("Nsfw", __file__)


@cog_i18n(_)
class Core(commands.Cog):

    __author__ = ["Predä", "aikaterna"]
    __version__ = "2.3.970"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def __init__(self, bot: Red):
        self.bot = bot
        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": (
                    f"Red-DiscordBot PredaCogs-Nsfw/{self.__version__} "
                    f"(Python/{'.'.join(map(str, sys.version_info[:3]))} aiohttp/{aiohttp.__version__})"
                )
            }
        )
        self.config = Config.get_conf(self, identifier=512227974893010954, force_registration=True)
        self.config.register_global(use_reddit_api=False)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    async def _get_imgs(self, subs: List[str] = None):
        """Get images from Reddit API."""
        tries = 0
        while tries < 5:
            sub = choice(subs)
            try:
                if await self.config.use_reddit_api():
                    async with self.session.get(REDDIT_BASEURL.format(sub=sub)) as reddit:
                        if reddit.status != 200:
                            return None, None
                        try:
                            data = await reddit.json(content_type=None)
                            content = data[0]["data"]["children"][0]["data"]
                            url = content["url"]
                            subr = content["subreddit"]
                        except (KeyError, ValueError, json.decoder.JSONDecodeError):
                            tries += 1
                            continue
                        if url.startswith(IMGUR_LINKS):
                            url = url + ".png"
                        elif url.endswith(".mp4"):
                            url = url[:-3] + "gif"
                        elif url.endswith(".gifv"):
                            url = url[:-1]
                        elif not url.endswith(GOOD_EXTENSIONS) and not url.startswith(
                            "https://gfycat.com"
                        ):
                            tries += 1
                            continue
                        return url, subr
                else:
                    async with self.session.get(
                        MARTINE_API_BASE_URL, params={"name": sub}
                    ) as resp:
                        if resp.status != 200:
                            tries += 1
                            continue
                        try:
                            data = await resp.json()
                            return data["data"]["image_url"], data["data"]["subreddit"]["name"]
                        except (KeyError, json.JSONDecodeError):
                            tries += 1
                            continue
            except aiohttp.client_exceptions.ClientConnectionError:
                tries += 1
                continue

        return None, None

    async def _get_others_imgs(self, ctx: commands.Context, url: str = None):
        """Get images from all other images APIs."""
        try:
            async with self.session.get(url) as resp:
                if resp.status != 200:
                    await self._api_errors_msg(ctx, error_code=resp.status)
                    return None
                try:
                    data = await resp.json(content_type=None)
                except json.decoder.JSONDecodeError as exception:
                    await self._api_errors_msg(ctx, error_code=exception)
                    return None
            data = dict(img=data)
            return data
        except aiohttp.client_exceptions.ClientConnectionError:
            await self._api_errors_msg(ctx, error_code="JSON decode failed")
            return None

    async def _api_errors_msg(self, ctx: commands.Context, error_code: int = None):
        """Error message when API calls fail."""
        return await ctx.send(
            _("Error when trying to contact image service, please try again later. ")
            + "(Code: {})".format(inline(str(error_code)))
        )

    async def _version_msg(self, ctx: commands.Context, version: str, authors: List[str]):
        """Cog version message."""
        msg = box(
            _("Nsfw cog version: {version}\nAuthors: {authors}").format(
                version=version, authors=", ".join(authors)
            ),
            lang="py",
        )
        return await ctx.send(msg)

    async def _make_embed(self, ctx: commands.Context, subs: List[str], name: str):
        """Function to make the embed for all Reddit API images."""
        try:
            url, subr = await asyncio.wait_for(self._get_imgs(subs=subs), 3)
        except asyncio.TimeoutError:
            await ctx.send("Failed to get an image. Please try again later. (Timeout error)")
            return
        if not url:
            return
        if url.endswith(GOOD_EXTENSIONS):
            em = await self._embed(
                color=0x891193,
                title=(_("Here is {name} image ...") + " \N{EYES}").format(name=name),
                description=bold(
                    _("[Link if you don't see image]({url})").format(url=url),
                    escape_formatting=False,
                ),
                image=url,
                footer=_("Requested by {req} {emoji} • From r/{r}").format(
                    req=ctx.author.display_name, emoji=emoji(), r=subr
                ),
            )
        if url.startswith("https://gfycat.com"):
            em = (
                _("Here is {name} gif ...")
                + " \N{EYES}\n\n"
                + _("Requested by {req} {emoji} • From {r}\n{url}")
            ).format(
                name=name,
                req=bold(ctx.author.display_name),
                emoji=emoji(),
                r=bold(f"r/{subr}"),
                url=url,
            )
        return em

    async def _make_embed_other(
        self, ctx: commands.Context, name: str, url: str, arg: str, source: str
    ):
        """Function to make the embed for all others APIs images."""
        try:
            data = await asyncio.wait_for(self._get_others_imgs(ctx, url=url), 3)
        except asyncio.TimeoutError:
            await ctx.send("Failed to get an image. Please try again later. (Timeout error)")
            return
        if not data:
            return
        em = await self._embed(
            color=0x891193,
            title=(_("Here is {name} image ...") + " \N{EYES}").format(name=name),
            description=bold(
                _("[Link if you don't see image]({url})").format(url=data["img"][arg]),
                escape_formatting=False,
            ),
            image=data["img"][arg],
            footer=_("Requested by {req} {emoji} • From {source}").format(
                req=ctx.author.display_name, emoji=emoji(), source=source
            ),
        )
        return em

    async def _maybe_embed(self, ctx: commands.Context, embed: Union[discord.Embed, str]):
        """
        Function to choose if type of the message is an embed or not
        and if not send a simple message.
        """
        try:
            if isinstance(embed, discord.Embed):
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed)
        except discord.HTTPException:
            return

    async def _send_msg(self, ctx: commands.Context, name: str, subs: List[str] = None):
        """Main function called in all Reddit API commands."""
        embed = await self._make_embed(ctx, subs, name)
        return await self._maybe_embed(ctx, embed=embed)

    async def _send_other_msg(
        self, ctx: commands.Context, name: str, arg: str, source: str, url: str = None
    ):
        """Main function called in all others APIs commands."""
        embed = await self._make_embed_other(ctx, name, url, arg, source)
        return await self._maybe_embed(ctx, embed)

    @staticmethod
    async def _embed(
        color: Union[int, discord.Color] = None,
        title: str = None,
        description: str = None,
        image: str = None,
        footer: Optional[str] = None,
    ):
        em = discord.Embed(color=color, title=title, description=description)
        em.set_image(url=image)
        if footer:
            em.set_footer(text=footer)
        return em
