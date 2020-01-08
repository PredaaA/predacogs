import discord

from redbot.core import Red
from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import humanize_timedelta

from datetime import datetime

import contextlib

_ = Translator("DblTools", __file__)


@cog_i18n(_)
class Converters(commands.Cog):
    """Some converters."""

    __author__ = "Predä"
    __version__ = "0.3.0"

    def __init__(self, bot: Red):
        self.bot = bot

    @commands.group(aliases=["converter"])
    async def conv(self, ctx: commands.Context):
        """Some utility converters."""
        pass

    @conv.command()
    async def todate(self, ctx: commands.Context, timestamp: int):
        """Convert a unix timestamp to a readable datetime."""
        try:
            given = timestamp[: timestamp.find(".")] if "." in timestamp else timestamp
            convert = datetime.utcfromtimestamp(int(given)).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, OverflowError):
            return await ctx.send(_("`{}` is not a valid timestamp.").format(given))
        g = datetime.fromtimestamp(int(given))
        curr = datetime.fromtimestamp(int(datetime.now().timestamp()))
        secs = str((curr - g).total_seconds())
        seconds = secs[1:][:-2] if "-" in secs else secs[:-2] if ".0" in secs else secs
        delta = humanize_timedelta(seconds=int(seconds))
        when = (
            _("It will be in {}.").format(delta) if g > curr else _("It was {} ago.").format(delta)
        )

        await ctx.send(
            _("Successfully converted `{given}` to `{convert}`\n{when}").format(
                given=given, convert=convert, when=when
            )
        )

    @conv.command()
    async def tounix(self, ctx: commands.Context, *, date: str):
        """
            Convert a date to a unix timestamp.

            Note: Need to respect this pattern `%Y-%m-%d %H:%M:%S`.
            Year-month-day Hour:minute:second
            Minimum to work is Year.
        """
        patterns = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d %H",
            "%Y-%m-%d",
            "%Y-%m",
            "%Y",
            "%m",
            "%d",
        ]
        for pattern in patterns:
            with contextlib.suppress(ValueError):
                convert = int(datetime.strptime(date, pattern).timestamp())
            if None:
                break
        try:
            given = datetime.fromtimestamp(int(convert))
        except UnboundLocalError:
            return await ctx.send(_("`{}` is not a valid timestamp.").format(date))
        curr = datetime.fromtimestamp(int(datetime.now().timestamp()))
        secs = str((curr - given).total_seconds())
        seconds = secs[1:][:-2] if "-" in secs else secs[:-2] if ".0" in secs else secs
        delta = humanize_timedelta(seconds=int(seconds))
        when = (
            _("It will be in {}.").format(delta)
            if given > curr
            else _("It was {} ago.").format(delta)
        )

        await ctx.send(
            _("Successfully converted `{date}` to `{convert}`\n{when}").format(
                date=date, convert=convert, when=when
            )
        )

    @conv.group(aliases=["c"])
    async def celsius(self, ctx: commands.Context):
        """
            Convert degree Celsius to Fahrenheit or Kelvin.
            See correct usage bellow.

            Usage:
            To Fahrenheit: `[p]convert celsius fahrenheit`
            To Kelvin: `[p]convert celsius kelvin`
            (You can also use `[p]convert c f` or `[p]convert c k`)
        """
        pass

    @celsius.command(name="fahrenheit", aliases=["f"])
    async def celsius_to_fahrenheit(self, ctx: commands.Context, temperature: float):
        """Convert degree Celsius to Fahrenheit."""
        if not temperature:
            return await ctx.send_help()
        fahrenheit = round((temperature * 1.8) + 32, 1)
        msg = _("{temp:,}° Celsius is equal to {f:,}° Fahrenheit.").format(
            temp=temperature, f=fahrenheit
        )
        await ctx.send(msg)

    @celsius.command(name="kelvin", aliases=["k"])
    async def celsius_to_kelvin(self, ctx: commands.Context, temperature: float):
        """Convert degree Celsius to Kelvin."""
        if not temperature:
            return await ctx.send_help()
        kelvin = round((temperature + 273.15), 1)
        msg = _("{temp:,}° Celsius is equal to {k:,}° Kelvin.").format(temp=temperature, k=kelvin)
        await ctx.send(msg)

    @conv.group(aliases=["f"])
    async def fahrenheit(self, ctx: commands.Context):
        """
            Convert Fahrenheit degree to Celsius or Kelvin.
            See correct usage bellow.

            Usage:
            To Celsius: `[p]convert fahrenheit celsius`
            To Kelvin: `[p]convert fahrenheit kelvin`
            (You can also use `[p]convert f c` or `[p]convert f k`)
        """
        pass

    @fahrenheit.command(name="celsius", aliases=["c"])
    async def fahrenheit_to_celsius(self, ctx: commands.Context, temperature: float):
        """Convert Fahrenheit degree to Celsius."""
        if not temperature:
            return await ctx.send_help()
        celsius = round((temperature - 32) / 1.8, 1)
        msg = _("{temp:,}° Fahrenheit is equal to {c:,}° Celsius.").format(
            temp=temperature, c=celsius
        )
        await ctx.send(msg)

    @fahrenheit.command(name="kelvin", aliases=["k"])
    async def fahrenheit_to_kelvin(self, ctx: commands.Context, temperature: float):
        """Convert Fahrenheit degree to Kelvin."""
        if not temperature:
            return await ctx.send_help()
        kelvin = round((temperature - 32) * (5 / 9) + 273.15, 1)
        msg = _("{temp:,}° Fahrenheit is equal to {k:,}° Kelvin.").format(
            temp=temperature, k=kelvin
        )
        await ctx.send(msg)

    @conv.group(aliases=["k"])
    async def kelvin(self, ctx: commands.Context):
        """
            Convert Kelvin degree to Celsius or Fahrenheit.
            See correct usage bellow.

            Usage:
            To Celsius: `[p]convert kelvin celsius`
            To Fahrenheit: `[p]convert kelvin fahrenheit`
            (You can also use `[p]convert f c` or `[p]convert f k`)
        """
        pass

    @kelvin.command(name="celsius", aliases=["c"])
    async def kelvin_to_celsius(self, ctx: commands.Context, temperature: float):
        """Convert Kelvin degree to Celsius."""
        if not temperature:
            return await ctx.send_help()
        celsius = round((temperature - 273.15) * (9 / 5) + 32, 1)
        msg = _("{temp:,}° Kelvin is equal to {c:,}° Celsius.").format(temp=temperature, c=celsius)
        await ctx.send(msg)

    @kelvin.command(name="fahrenheit", aliases=["f"])
    async def kelvin_to_fahrenheit(self, ctx: commands.Context, temperature: float):
        """Convert Kelvin degree to Fahrenheit."""
        if not temperature:
            return await ctx.send_help()
        fahrenheit = round((temperature - 273.15), 1)
        msg = _("{temp:,}° Kelvin is equal to {f:,}° Fahrenheit.").format(
            temp=temperature, f=fahrenheit
        )
        await ctx.send(msg)

    @conv.command(aliases=["lb"])
    async def pounds(self, ctx: commands.Context, mass: float):
        """Convert pounds to kilograms."""
        kg = round((mass * 0.45359237), 1)
        await ctx.send(_("{mass:,} lb is equal to {kg:,} kg.").format(mass=mass, kg=kg))

    @conv.command(aliases=["kg"])
    async def kilograms(self, ctx: commands.Context, mass: float):
        """Convert kilograms to pounds."""
        lb = round((mass / 0.45359237), 1)
        await ctx.send(_("{mass:,} kg is equal to {lb:,} lb.").format(mass=mass, lb=lb))

    @conv.command(aliases=["mi"])
    async def miles(self, ctx: commands.Context, length: float):
        """Convert miles to kilometers."""
        km = round((length * 1.609344), 1)
        await ctx.send(_("{length:,} mi is equal to {km:,} km.").format(length=length, km=km))

    @conv.command(aliases=["km"])
    async def kilometers(self, ctx: commands.Context, length: float):
        """Convert kilometers to miles."""
        mi = round((length / 1.609344), 1)
        await ctx.send(_("{length:,} km is equal to {mi:,} mi.").format(length=length, mi=mi))
