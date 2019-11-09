import discord

from redbot.core import commands, Config, checks
from redbot.core.utils.chat_formatting import box, inline

import aiohttp
import asyncio


class FiveM(commands.Cog):
    """Tools for FiveM servers."""

    __author__ = "Predä"
    __version__ = "0.1"

    def __init__(self, bot):
        self.bot = bot

        self.config = Config.get_conf(self, 33298047065037209654, force_registration=True)
        self.config.register_global(
            ip=None,
            toggled=False,
            text="{players}/{total} players are connected on {server_ip}!",
            status="online",
            activity_type="playing",
            streamer=None,
            stream_title=None,
        )

        self.session = aiohttp.ClientSession()
        self.status_task = bot.loop.create_task(self._change_bot_status())

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
        self.status_task.cancel()

    @staticmethod
    def _status(key: str):
        statuses = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "invisible": discord.Status.invisible,
        }
        try:
            return statuses[key]
        except KeyError:
            return statuses

    @staticmethod
    def _activity_types(key: str):
        types = {
            "playing": discord.ActivityType.playing,
            "watching": discord.ActivityType.watching,
            "listening": discord.ActivityType.listening,
        }
        try:
            return types[key]
        except KeyError:
            return types

    @staticmethod
    def _format_text_status(data_players: dict, data_server: dict, config_data: dict) -> dict:
        return dict(
            players=len(data_players),
            total=data_server["vars"]["sv_maxClients"],
            server_ip=config_data["ip"],
        )

    async def _set_default_status(self, config_data: dict):
        await self.bot.change_presence(status=self._status(config_data["status"]))

    async def _get_data(self, ip: str, endpoint: str):
        try:
            try:
                async with self.session.get(f"http://{ip}/{endpoint}.json") as resp:
                    if resp.status != 200:
                        return None
                    data = await resp.json(content_type=None, encoding="utf-8")
                    return data
            except Exception as error:
                print(error)
                return None
        except aiohttp.client_exceptions.ClientConnectionError:
            return None

    async def _get_config_data(self):
        async with self.config.all() as config:
            return config

    async def _change_bot_status(self):
        await self.bot.wait_until_ready()
        while True:
            await asyncio.sleep(10)
            config_data = await self._get_config_data()
            if not config_data["toggled"]:
                # await self._set_default_status(config_data)
                continue
            if config_data["ip"] is None:
                continue
            data_players = await self._get_data(config_data["ip"], "players")
            data_server = await self._get_data(config_data["ip"], "info")
            if data_players is None or data_server is None:
                await self._set_default_status(config_data)
                continue
            activity = discord.Activity(
                name=config_data["text"].format(
                    **self._format_text_status(data_players, data_server, config_data)
                ),
                type=self._activity_types(config_data["activity_type"]),
            )
            if config_data["activity_type"] == "streaming":
                activity = discord.Streaming(
                    url=config_data["streamer"],
                    name=config_data["stream_title"].format(
                        **self._format_text_status(data_players, data_server, config_data)
                    ),
                )
            await self.bot.change_presence(
                status=self._status(config_data["status"]), activity=activity
            )

    @checks.is_owner()
    @commands.group()
    async def fivemset(self, ctx: commands.Context):
        """Commands group for FiveM cog."""
        if not ctx.invoked_subcommand:
            # Logic from Trusty's welcome.py https://github.com/TrustyJAID/Trusty-cogs/blob/master/welcome/welcome.py#L71
            # TODO This is just a first approach to show current settings.
            settings = await self.config.get_raw()
            settings_name = dict(
                toggled="Custom status toggled:",
                ip="FiveM IP address:",
                text="Custom status text:",
                status="Custom status:",
                activity_type="Activity type:",
                streamer="Streamer:",
                stream_title="Stream title:",
            )
            if ctx.channel.permissions_for(ctx.me).embed_links:
                em = discord.Embed(
                    color=await ctx.embed_colour(), title=f"FiveM settings for {self.bot.user}"
                )
                msg = ""
                for attr, name in settings_name.items():
                    if attr == "toggled":
                        if settings[attr]:
                            msg += f"**{name}** Yes\n"
                        else:
                            msg += f"**{name}** No\n"
                    elif attr == "ip":
                        if settings[attr]:
                            msg += f"**{name}** {inline(settings[attr])}\n"
                        else:
                            msg += f"**{name}** Not set\n"
                    elif attr == "text":
                        if settings[attr]:
                            msg += f"**{name}**\n{inline(settings[attr])}\n"
                        else:
                            msg += f"**{name}** Not set\n"
                    elif attr == "streamer":
                        if settings[attr]:
                            msg += f"**{name}** {inline(settings[attr])}\n"
                        else:
                            msg += f"**{name}** Not set\n"
                    elif attr == "stream_title":
                        if settings[attr]:
                            msg += f"**{name}** {inline(settings[attr])}\n"
                        else:
                            msg += f"**{name}** Not set\n"
                    else:
                        msg += f"**{name}** {inline(settings[attr])}\n"
                em.description = msg
                await ctx.send(embed=em)
            else:
                msg = "```\n"
                for attr, name in settings_name.items():
                    if attr == "toggled":
                        if settings[attr]:
                            msg += f"{name} Yes\n"
                        else:
                            msg += f"{name} No\n"
                    elif attr == "ip":
                        if settings[attr]:
                            msg += f"{name} {settings[attr]}\n"
                        else:
                            msg += f"{name} Not set\n"
                    elif attr == "text":
                        if settings[attr]:
                            msg += f"{name}\n{settings[attr]}\n"
                        else:
                            msg += f"{name} Not set\n"
                    elif attr == "streamer":
                        if settings[attr]:
                            msg += f"{name} {settings[attr]}\n"
                        else:
                            msg += f"**{name}** Not set\n"
                    elif attr == "stream_title":
                        if settings[attr]:
                            msg += f"{name} {settings[attr]}\n"
                        else:
                            msg += f"{name} Not set\n"
                    else:
                        msg += f"{name} {settings[attr]}\n"
                msg += "```"
                await ctx.send(msg)

    @fivemset.command()
    async def ip(self, ctx: commands.Context, *, ip: str):
        """
        Choose which FiveM server you want to get data.

        This needs to be an IP address with a port.
        Example: `1.2.3.4:30122`
        """
        ip = ip.replace("http://", "").replace("/", "")
        await self.config.ip.set(ip)
        await ctx.send(f"FiveM server set to: {inline(ip)}")

    @fivemset.command()
    async def toggle(self, ctx: commands.Context):
        """Choose if you want to have a custom status based on a selected FiveM server."""
        toggled = await self.config.toggled()
        await self.config.toggled.set(not toggled)
        msg = (
            "I will no longer show a custom status based on a FiveM server. Use the same command to set it back."
            if toggled
            else f"I will now show a custom status based on a FiveM server.\nMake sure to set a valid IP address using `{ctx.prefix}fivemset ip` command!"
        )
        await ctx.send(msg)

    @fivemset.command()
    async def text(self, ctx: commands.Context, *, text: str):
        """
        Choose a custom text for the bot status.

        You can use some arguments:
        - `{players}` will show how many players are connected.
        - `{total}` will show the total players the server can have.
        - `{server_ip}` will show the server ip.

        Default is: `{players}/{total} players are connected on {server_ip}!`
        """
        await self.config.text.set(text)
        await ctx.send(f"Custom status text set to: {inline(text)}")

    @fivemset.command()
    async def status(self, ctx: commands.Context, *, status: str):
        """
        Choose which status you want to see for the bot status.

        Available statuses:
        - online
        - idle
        - dnd
        """
        statuses = ["online", "dnd", "idle"]
        if not status.lower() in statuses:
            await ctx.send_help()
            return

        await self.config.status.set(status.lower())
        await ctx.send(f"Status set to: {inline(status.lower())}")

    @fivemset.command()
    async def activitytype(self, ctx: commands.Context, *, activity: str):
        """
        Choose which type of activity you want to see for the bot status.

        Available types:
        - playing
        - watching
        - listening
        """
        activity_types = ["playing", "watching", "listening"]
        if not activity.lower() in activity_types:
            await ctx.send_help()
            return

        await self.config.activity_type.set(activity.lower())
        await ctx.send(f"Activity type set to: {inline(activity.lower())}")

    @fivemset.command()
    async def activitystream(self, ctx: commands.Context, streamer=None, *, streamtitle=None):
        """
        Choose if you want to put a Twitch stream for the bot status.

        Example: `[p]fivemset activitystream summit1g Come watch my stream!`

        You can use some arguments:
        - `{players}` will show how many players are connected.
        - `{total}` will show the total players the server can have.
        - `{server_ip}` will show the server ip.

        Advanced example: `[p]fivemset activitystream summit1g {players}/{total} players are connected on LifeRP, check out my stream!`
        """
        # Some logics from https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/core/core_commands.py#L1017
        if streamtitle:
            streamtitle = streamtitle.strip()
            if "twitch.tv/" not in streamer:
                streamer = "https://www.twitch.tv/" + streamer
            async with self.config.all() as config:
                config["streamer"] = streamer
                config["stream_title"] = streamtitle
                config["activity_type"] = "streaming"
            await ctx.send(
                "Activity stream set to:\n" + box(f"Streamer: {streamer}\nTitle   : {streamtitle}")
            )
        elif streamer is None or streamtitle is None:
            await ctx.send_help()
            return
