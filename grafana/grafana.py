import time
from datetime import datetime, timedelta
from io import BytesIO
from urllib.parse import quote

import aiohttp
import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.commands.converter import TimedeltaConverter
from redbot.core.utils.chat_formatting import box, humanize_list


from .utils import Panel


class Grafana(commands.Cog):

    __author__ = "Predä"
    __version__ = "1.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.config = Config.get_conf(self, identifier=0xEA016D013C7B488894399820F2BE9874)
        default_global = {
            "url": "http://localhost:3000",
            "dashboard_id": None,
            "panels": {},
        }
        self.config.register_global(**default_global)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"

    async def fetch_grafana(self, **kwargs):
        from_time = kwargs.get("timedelta")
        params = {
            "orgId": 1,
            "from": int((datetime.now() - from_time).timestamp()) * 1000,
            "to": int(time.time()) * 1000,
            "panelId": kwargs.get("panelid"),
            "width": 1000,
            "height": 500,
        }
        async with self.bot.session.get(
            f"{await self.config.url()}/render/d-solo/" f"{await self.config.dashboard_id()}",
            params=params,
        ) as resp:
            if resp.status != 200:
                return None, {}
            return BytesIO(await resp.read()), params

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, commands.BucketType.guild)
    async def graph(
        self,
        ctx: commands.Context,
        panel: Panel,
        from_time: TimedeltaConverter = timedelta(days=1),
    ):
        """Render an image of a selected panel of [botname] metrics."""
        async with ctx.typing():
            file, params = await self.fetch_grafana(panelid=panel.id, timedelta=from_time)
        if not file:
            return await ctx.send("Failed to fetch Grafana.")
        msg = (
            f"{await self.config.url()}/d/{await self.config.dashboard_id()}?"
            f"panelId={params['panelId']}&fullscreen&orgId={params['orgId']}"
            f"&from={params['from']}&to={params['to']}&refresh=15m"
        )
        filename = "&".join([f"{k}={v}" for k, v in params.items()])
        return await ctx.send(msg, file=discord.File(file, filename=f"graph-{filename}.png"))

    @graph.command(name="list")
    async def list_graphs(self, ctx: commands.Context):
        """List all panels that can be used with `[p]graph` command."""
        if panels := await self.config.panels():
            await ctx.send(box(humanize_list(list(panels.keys()))))
        else:
            await ctx.send("No panels configured")

    @graph.group(name="set")
    @commands.is_owner()
    async def set_graphs(self, ctx):
        """Setup grafana cog."""
        pass

    @set_graphs.command(name="url")
    async def grafana_url(self, ctx, *, url: str):
        """Setup url of your Grafana instance.

        Default: `http://localhost:3000`"""
        await self.config.url.set(url)
        await ctx.tick()

    @set_graphs.command()
    async def dashboard(self, ctx, *, did: str):
        """Set dashboard id.

        This command needs id from URL.
        Example: ```
        http://localhost:3000/d/AbCdEf0G/dashboard
                                ^ here ^
        ```"""
        async with self.session.get(f"{await self.config.url()}/api/dashboards/uid/{did}") as r:
            try:
                rj = await r.json()
            except aiohttp.ContentTypeError:
                rj = {}
            if r.status != 200:
                await ctx.send(
                    f"Unable to found provided dashboard: {rj.get('message') or 'Unknown error, did you set up an url?'}"
                )
                return
        await self.config.dashboard_id.set(did)
        await ctx.tick()

    @set_graphs.group()
    async def panels(self, ctx):
        """Setup graphs on dashboard."""
        pass

    @panels.command(name="import")
    @commands.max_concurrency(1)
    async def graphs_import(self, ctx):
        """Automatically import all graphs from dashboard, overwriting already saved."""
        try:
            async with self.bot.session.get(
                f"{await self.config.url()}/api/dashboards/uid/{await self.config.dashboard_id()}",
                raise_for_status=True,
            ) as r:
                r = await r.json()
                await self.config.panels.set(
                    {
                        p["title"].casefold().replace(" ", "_"): p["id"]
                        for p in r["dashboard"]["panels"]
                        if p["type"] != "row"
                    }
                )
                await ctx.tick()
        except aiohttp.ClientResponseError as e:
            await ctx.send(
                f"Unable to import graphs, are url and dashboard set?\n{e.status}: {e.message}"
            )
        except aiohttp.ClientConnectorError as e:
            await ctx.send(
                f"Unable to import graphs, are url and dashboard set?"
            )

    @panels.command(name="remove")
    async def graphs_remove(self, ctx, *, panel: Panel):
        """Remove certain graph from list"""
        async with self.config.panels() as panels:
            del panels[panel.name]
        await ctx.tick()

    @panels.command(name="add")
    async def graphs_add(self, ctx, pid: int, *, name: str):
        """Add certain graph to list manually"""
        async with self.config.panels() as panels:
            panels[name.casefold().replace(" ", "_")] = pid
        await ctx.tick()
