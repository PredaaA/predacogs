import time
from datetime import datetime, timedelta
from io import BytesIO
from typing import Optional

import aiohttp
import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.commands.converter import TimedeltaConverter
from redbot.core.utils.chat_formatting import box, humanize_list
from tabulate import tabulate

from .utils import Panel, find_panel


class Grafana(commands.Cog):
    """Grafana graphs in your Discord!"""

    __author__ = ["Predä", "Fixator10"]
    __version__ = "1.0.1"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def __init__(self, bot: Red):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.config = Config.get_conf(self, identifier=0xEA016D013C7B488894399820F2BE9874)
        self.config.register_global(url="http://localhost:3000", dashboard_id=None, panels={})

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    async def fetch_grafana(self, **kwargs):
        from_time = kwargs.get("timedelta")
        params = {
            "orgId": 1,
            "from": int((datetime.now() - from_time).timestamp()) * 1000,
            "to": int(time.time()) * 1000,
            "panelId": kwargs.get("panelid"),
            "width": 1000,
            "height": 500,
            "tz": "UTC",
        }
        try:
            async with self.session.get(
                f"{await self.config.url()}/render/d-solo/{await self.config.dashboard_id()}",
                params=params,
            ) as resp:
                if resp.status != 200:
                    return None, {}
                return BytesIO(await resp.read()), params
        except aiohttp.ClientConnectionError:
            return None, {}

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, commands.BucketType.guild)
    async def graph(
        self,
        ctx: commands.Context,
        from_time: Optional[TimedeltaConverter] = timedelta(days=1),
        *,
        panel: Panel,
    ):
        """Render an image of a selected panel of [botname] metrics."""
        async with ctx.typing():
            file, params = await self.fetch_grafana(panelid=panel.id, timedelta=from_time)
        if not file:
            return await ctx.send("Failed to fetch Grafana.")
        msg = (
            f"{await self.config.url()}/d/{await self.config.dashboard_id()}?"
            f"panelId={params['panelId']}&fullscreen&orgId={params['orgId']}"
            f"&from={params['from']}&to={params['to']}"
        )
        filename = "&".join(f"{k}={v}" for k, v in params.items())
        return await ctx.send(msg, file=discord.File(file, filename=f"graph-{filename}.png"))

    @graph.command(name="list")
    async def list_graphs(self, ctx: commands.Context):
        """List all panels that can be used with `[p]graph` command."""
        if panels := await self.config.panels():
            await ctx.send(box(humanize_list(list(panels.keys()))))
        else:
            await ctx.send("No panels configured.")

    @graph.group(name="set")
    @commands.is_owner()
    async def set_graphs(self, ctx: commands.Context):
        """Setup grafana cog."""

    @set_graphs.command(name="showsettings", aliases=["settings"])
    async def graphs_settings(self, ctx: commands.Context):
        """Show current settings."""
        config_without_panels = await self.config.all()
        del config_without_panels["panels"]
        await ctx.send(box(tabulate(config_without_panels.items())))

    @set_graphs.command(name="url")
    async def grafana_url(self, ctx: commands.Context, *, url: str):
        """Setup url of your Grafana instance.

        Default: `http://localhost:3000`"""
        if not url.startswith("http"):
            url = "http://" + url
        url = url.rstrip("/")
        async with ctx.typing():
            try:
                async with self.session.get(f"{url}/api/health") as r:
                    if r.status != 200:
                        await ctx.send(f"Incorrect URL. HTTP error returned: {r.status}")
                        return
                    try:
                        if j := await r.json():
                            if j.get("database") != "ok":
                                await ctx.send(
                                    "API didnt returned right state of DB, is your Grafana ok?"
                                )
                                return
                        else:
                            await ctx.send(
                                "That URL hasn't returned a JSON. Is it a Grafana server?"
                            )
                            return
                    except aiohttp.ContentTypeError:
                        await ctx.send("That URL hasn't returned a JSON. Is it a Grafana server?")
                        return
            except aiohttp.InvalidURL:
                await ctx.send("This is not a valid URL. Check your input and try again.")
                return
            except aiohttp.ClientConnectorError:
                await ctx.send("Server did not respond. Check your input and try again.")
                return
        await self.config.url.set(url)
        await ctx.send(
            f"Don't forget to setup dashboard via `{ctx.clean_prefix}graph set dashboard` too.\n"
            f"After that you can use `{ctx.clean_prefix}graph set panels import` to import your panels."
        )

    @set_graphs.command()
    async def dashboard(self, ctx: commands.Context, *, did: str):
        """Set dashboard id.

        This command needs id from URL.
        Example: ```
        http://localhost:3000/d/AbCdEf0G/dashboard
                                ^ here ^
        ```"""
        try:
            async with self.session.get(
                f"{await self.config.url()}/api/dashboards/uid/{did}"
            ) as r:
                try:
                    rj = await r.json()
                except aiohttp.ContentTypeError:
                    rj = {}
                if r.status != 200:
                    await ctx.send(
                        "Unable to found provided dashboard: "
                        f"{rj.get('message') or 'Unknown error, did you set up an url?'}"
                    )
                    return
        except aiohttp.ClientConnectorError:
            await ctx.send("Server did not respond. Make sure that URL setting is set correctly.")
            return
        await self.config.dashboard_id.set(did)
        await ctx.send(
            f"Make sure that you setup URL via `{ctx.clean_prefix}graph set url`.\n"
            f"After that you can use `{ctx.clean_prefix}graph set panels import` to import your panels."
        )

    @set_graphs.group()
    async def panels(self, ctx: commands.Context):
        """Setup graphs on dashboard."""

    @panels.command(name="import")
    @commands.max_concurrency(1)
    async def graphs_import(self, ctx: commands.Context):
        """Automatically import all graphs from dashboard, overwriting already saved."""
        try:
            async with self.session.get(
                f"{await self.config.url()}/api/dashboards/uid/{await self.config.dashboard_id()}",
                raise_for_status=True,
            ) as r:
                r = await r.json()
                await self.config.panels.set(
                    {
                        p["title"].casefold().replace(" ", "_") or f"panel_{p['id']}": p["id"]
                        for p in r["dashboard"]["panels"]
                        if p["type"] != "row"
                    }
                )
                await ctx.tick()
        except aiohttp.ClientResponseError as e:
            await ctx.send(
                f"Unable to import graphs, are URL and dashboard ID set?\n{e.status}: {e.message}"
            )
        except aiohttp.ClientConnectorError:
            await ctx.send(f"Unable to import graphs, are URL and dashboard ID set?")

    @panels.command(name="remove")
    async def graphs_remove(self, ctx: commands.Context, *, panel: Panel):
        """Remove certain graph from list."""
        async with self.config.panels() as panels:
            del panels[panel.name]
        await ctx.tick()

    @panels.command(name="add")
    async def graphs_add(self, ctx: commands.Context, pid: int, *, name: str):
        """Add certain graph to list manually."""
        try:
            async with self.session.get(
                f"{await self.config.url()}/api/dashboards/uid/{await self.config.dashboard_id()}",
                raise_for_status=True,
            ) as r:
                r = await r.json()
                if not await find_panel(r["dashboard"]["panels"], pid):
                    await ctx.send("This panel is not found on current set dashboard.")
                    return
        except aiohttp.ClientResponseError as e:
            await ctx.send(
                f"Unable to import graphs, are URL and dashboard ID set?\n{e.status}: {e.message}"
            )
        except aiohttp.ClientConnectorError:
            await ctx.send(f"Unable to import graphs, are URL and dashboard ID set?")
        async with self.config.panels() as panels:
            panels[name.casefold().replace(" ", "_")] = pid
        await ctx.tick()
