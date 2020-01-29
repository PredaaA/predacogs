import discord

from redbot.core import commands
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS

from .core import Core

from random import choice
from typing import Optional


class SpaceX(Core, commands.Cog):
    """Get multiple information about SpaceX using SpaceX-API."""

    __author__ = "Predä"
    __version__ = "0.1.3"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"

    @commands.group()
    async def spacex(self, ctx):
        """SpaceX group commands."""
        pass

    @spacex.command()
    @commands.bot_has_permissions(embed_links=True)
    async def about(self, ctx):
        """Send general company information about SpaceX."""

        await self._about(ctx)

    @spacex.command()
    @commands.bot_has_permissions(embed_links=True)
    async def aboutcog(self, ctx):
        """Send information about the cog and SpaceX-API."""

        await self._about_cog(ctx, version=self.__version__)

    @spacex.command()
    @commands.bot_has_permissions(embed_links=True)
    async def history(self, ctx):
        """Return SpaceX historical events."""
        async with ctx.typing():
            resp = await self._get_data(ctx, "history")
            if resp is None:
                return

            msg = []
            page = 1
            for data in resp:
                description = await self._history_texts(data)
                em = discord.Embed(
                    color=await ctx.embed_colour(),
                    title=data["title"],
                    description=data["details"],
                )
                em.add_field(name="Infos:", value=description)
                em.set_footer(text="Page {} of {}".format(page, len(resp)))
                page += 1
                msg.append(em)

        await menu(ctx, msg, DEFAULT_CONTROLS)

    @spacex.command()
    @commands.bot_has_permissions(embed_links=True)
    async def launchpads(self, ctx):
        """Return SpaceX launchpads."""
        async with ctx.typing():
            resp = await self._get_data(ctx, "launchpads")
            if resp is None:
                return

            msg = []
            page = 1
            for data in resp:
                description = await self._launchpads_texts(data)
                em = discord.Embed(
                    color=await ctx.embed_colour(),
                    title=data["location"]["name"],
                    description=data["details"]
                    + "\n**[Wikipedia page]({})**".format(data["wikipedia"]),
                )
                em.add_field(name="Infos:", value=description)
                em.set_footer(text="Page {} of {}".format(page, len(resp)))
                page += 1
                msg.append(em)

        await menu(ctx, msg, DEFAULT_CONTROLS)

    @spacex.command()
    @commands.bot_has_permissions(embed_links=True)
    async def landpads(self, ctx):
        """Return SpaceX landpads."""
        async with ctx.typing():
            resp = await self._get_data(ctx, "landpads")
            if resp is None:
                return

            msg = []
            page = 1
            for data in resp:
                description = await self._landpads_texts(data)
                em = discord.Embed(
                    color=await ctx.embed_colour(),
                    title="Name: {name} • ID: {id}".format(name=data["full_name"], id=data["id"]),
                    description=data["details"]
                    + "\n**[Wikipedia page]({})**".format(data["wikipedia"]),
                )
                em.add_field(name="Infos:", value=description)
                em.set_footer(text="Page {} of {}".format(page, len(resp)))
                page += 1
                msg.append(em)

        await menu(ctx, msg, DEFAULT_CONTROLS)

    @spacex.command()
    @commands.bot_has_permissions(embed_links=True)
    async def missions(self, ctx):
        """Returns all missions of SpaceX."""
        async with ctx.typing():
            resp = await self._get_data(ctx, "missions")
            if resp is None:
                return

            msg = []
            page = 1
            for data in resp:
                description = await self._missions_texts(data)
                manufacturers = ", ".join(data["manufacturers"])
                payloads = ", ".join(data["payload_ids"])
                em = discord.Embed(
                    color=await ctx.embed_colour(),
                    title="Name: {name} • ID: {id}".format(
                        name=data["mission_name"], id=data["mission_id"]
                    ),
                    description=description,
                )
                em.add_field(
                    name="Infos:",
                    value=(
                        "Manufacturer{s}: **{manufacturers}**\n" "Payloads IDs: **{payloads_ids}**"
                    ).format(
                        s="s" if len(data["manufacturers"]) >= 2 else "",
                        manufacturers=manufacturers,
                        payloads_ids=payloads,
                    ),
                )
                em.set_footer(text="Page {} of {}".format(page, len(resp)))
                page += 1
                msg.append(em)

        await menu(ctx, msg, DEFAULT_CONTROLS)

    @spacex.command()
    @commands.bot_has_permissions(embed_links=True)
    async def roadster(self, ctx):
        """Get informations about Tesla roadster launched in space."""
        async with ctx.typing():
            data = await self._get_data(ctx, "roadster")
            if data is None:
                return

            roadster_stats = await self._roadster_texts(data)
            em = discord.Embed(
                color=await ctx.embed_colour(),
                title=data["name"],
                description=data["details"]
                + "\n**[Wikipedia page]({})**".format(data["wikipedia"]),
            )
            em.add_field(name="Some stats:", value=roadster_stats)
            em.set_thumbnail(url=choice(data["flickr_images"]))
        await ctx.send(embed=em)

    @spacex.command()
    @commands.bot_has_permissions(embed_links=True)
    async def rocket(self, ctx, details: Optional[bool] = False, *, rocket):
        """
            Get informations about SpaceX rockets.

            `[details]`: Set to `True` for more details.
            `<rocket>`: Name of an actual SpaceX rocket.
        """
        if not rocket:
            return await ctx.send_help()
        async with ctx.typing():
            bfr = ["big falcon rocket", "Big Falcon Rocket"]
            if rocket in bfr:
                rocket = "bfr"
            rocket = rocket.lower()
            rocket = rocket.replace(" ", "")
            data = await self._get_data(ctx, "rockets/" + rocket)
            if data is None:
                return

            base_stats, stages_stats, payload_weights_stats, engines_stats = await self._rockets_texts(
                data
            )

            em = discord.Embed(
                color=await ctx.embed_colour(),
                title=data["rocket_name"],
                description=data["description"]
                + "\n**[Wikipedia page]({})**".format(data["wikipedia"]),
            )
            em.add_field(name="Some stats:" if not details else "Basic stats:", value=base_stats)
            if details:
                em.add_field(name="Stages:", value=stages_stats)
                em.add_field(name="Payloads:", value=payload_weights_stats)
                em.add_field(name="Engines:", value=engines_stats)
            em.set_thumbnail(url=choice(data["flickr_images"]))
            await ctx.send(embed=em)

    @spacex.command()
    async def rockets(self, ctx, details: bool = False):
        """
            Get informations of all SpaceX rockets.

            `[details]`: Set to True for more details.
        """
        async with ctx.typing():
            resp = await self._get_data(ctx, "rockets")
            if resp is None:
                return

            msg = []
            page = 1
            for data in resp:
                base_stats, stages_stats, payload_weights_stats, engines_stats = await self._rockets_texts(
                    data
                )

                em = discord.Embed(
                    color=await ctx.embed_colour(),
                    title=data["rocket_name"],
                    description=data["description"]
                    + "\n**[Wikipedia page]({})**".format(data["wikipedia"]),
                )
                em.add_field(
                    name="Some stats:" if not details else "Basic stats:", value=base_stats
                )
                if details:
                    em.add_field(name="Stages:", value=stages_stats)
                    em.add_field(name="Payloads:", value=payload_weights_stats)
                    em.add_field(name="Engines:", value=engines_stats)
                em.set_thumbnail(url=choice(data["flickr_images"]))
                em.set_footer(text="Page {} of {}".format(page, len(resp)))
                page += 1
                msg.append(em)

        await menu(ctx, msg, DEFAULT_CONTROLS)
