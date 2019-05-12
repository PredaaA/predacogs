import discord

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
    __version__ = "0.2"

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def convert(self, ctx):
        """Some utility converters."""
        pass

    @convert.command()
    async def todate(self, ctx, timestamp):
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

    @convert.command()
    async def tounix(self, ctx, *, date):
        """
            Convert a date to an unix timestamp.

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

    @convert.command(aliases=["celsiustofahrenheit", "ctof", "celsiustokelvin", "ctok"])
    async def celsius(self, ctx, temperature: float):
        """
            Convert degree Celsius to Fahrenheit or Kelvin.
            See correct usage bellow.

            Usage:
            To Fahrenheit: `[p]convert ctof`
            To Kelvin: `[p]convert ctok`
        """
        if not temperature:
            return await ctx.send_help()
        elif not ctx.invoked_with in ["celsiustofahrenheit", "ctof", "celsiustokelvin", "ctok"]:
            return await ctx.send_help()
        elif ctx.invoked_with in ["celsiustofahrenheit", "ctof"]:
            fahrenheit = round((temperature * 1.8) + 32, 1)
            msg = _("{temp:,}° Celsius is equal to {f:,}° Fahrenheit.").format(
                temp=temperature, f=fahrenheit
            )
        elif ctx.invoked_with in ["celsiustokelvin", "ctok"]:
            kelvin = round((temperature + 273.15), 1)
            msg = _("{temp:,}° Celsius is equal to {k:,}° Kelvin.").format(
                temp=temperature, k=kelvin
            )
        await ctx.send(msg)

    @convert.command(aliases=["fahrenheittocelsius", "ftoc", "fahrenheittokelvin", "ftok"])
    async def fahrenheit(self, ctx, temperature: float):
        """
            Convert Fahrenheit degree to Celsius or Kelvin.
            See correct usage bellow.

            Usage:
            To Celsius: `[p]convert ftoc`
            To Kelvin: `[p]convert ftok`
        """
        if not temperature:
            return await ctx.send_help()
        elif not ctx.invoked_with in ["fahrenheittocelsius", "ftoc", "fahrenheittokelvin", "ftok"]:
            return await ctx.send_help()
        elif ctx.invoked_with in ["fahrenheittocelsius", "ftoc"]:
            celsius = round((temperature - 32) / 1.8, 1)
            msg = _("{temp:,}° Fahrenheit is equal to {c:,}° Celsius.").format(
                temp=temperature, c=celsius
            )
        elif ctx.invoked_with in ["fahrenheittokelvin", "ftok"]:
            kelvin = round((temperature - 32) * (5 / 9) + 273.15, 1)
            msg = _("{temp:,}° Fahrenheit is equal to {k:,}° Kelvin.").format(
                temp=temperature, k=kelvin
            )
        await ctx.send(msg)

    @convert.command(aliases=["kelvintofahrenheit", "ktof", "kelvintocelsius", "ktoc"])
    async def kelvin(self, ctx, temperature: float):
        """
            Convert Kelvin degree to Fahrenheit or Celsius.
            See correct usage bellow.

            Usage:
            To Fahrenheit: `[p]convert ktof`
            To Celsius: `[p]convert ktoc`
        """
        if not temperature:
            return await ctx.send_help()
        elif not ctx.invoked_with in ["kelvintofahrenheit", "ktof", "kelvintocelsius", "ktoc"]:
            return await ctx.send_help()
        elif ctx.invoked_with in ["kelvintofahrenheit", "ktof"]:
            fahrenheit = round((temperature - 273.15) * (9 / 5) + 32, 1)
            msg = _("{temp:,}° Kelvin is equal to {f:,}° Fahrenheit.").format(
                temp=temperature, f=fahrenheit
            )
        elif ctx.invoked_with in ["kelvintocelsius", "ktoc"]:
            celsius = round((temperature - 273.15), 1)
            msg = _("{temp:,}° Kelvin is equal to {c:,}° Celsius.").format(
                temp=temperature, c=celsius
            )
        await ctx.send(msg)

    @convert.command(aliases=["lb"])
    async def pounds(self, ctx, mass: float):
        """Convert pounds to kilograms."""
        kg = round((mass * 0.45359237), 1)
        await ctx.send(_("{mass:,} lb is equal to {kg:,} kg.").format(mass=mass, kg=kg))

    @convert.command(aliases=["kg"])
    async def kilograms(self, ctx, mass: float):
        """Convert kilograms to pounds."""
        lb = round((mass / 0.45359237), 1)
        await ctx.send(_("{mass:,} kg is equal to {lb:,} lb.").format(mass=mass, lb=lb))

    @convert.command(aliases=["mi"])
    async def miles(self, ctx, lenght: float):
        """Convert miles to kilometers"""
        km = round((lenght * 1.609344), 1)
        await ctx.send(_("{lenght:,} mi is equal to {km:,} km.").format(lenght=lenght, km=km))

    @convert.command(aliases=["km"])
    async def kilometers(self, ctx, lenght: float):
        """Convert kilometers to miles."""
        mi = round((lenght / 1.609344), 1)
        await ctx.send(_("{lenght:,} km is equal to {mi:,} mi.").format(lenght=lenght, mi=mi))
