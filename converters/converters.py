import discord

from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_timedelta

from datetime import datetime

import contextlib


class Converters(commands.Cog):
    """Some converters."""

    __author__ = "Predä"
    __version__ = "0.1"

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
            return await ctx.send(f"`{given}` is not a valid timestamp.")
        b = datetime.fromtimestamp(int(given))
        curr = datetime.fromtimestamp(int(datetime.now().timestamp()))
        secs = str((curr - b).total_seconds())
        seconds = secs[1:][:-2] if "-" in secs else secs[:-2] if ".0" in secs else secs
        delta = humanize_timedelta(seconds=int(seconds))
        to = f"It will be in {delta}." if b > curr else f"It was {delta} ago."

        await ctx.send(f"Successfully converted `{given}` to `{convert}`\n{to}")

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
            with contextlib.suppress(ValueError): # TODO: Use the other thing Sinbad has sent.
                convert = int(datetime.strptime(date, pattern).timestamp())
            if None:
                break
        try:
            given = datetime.fromtimestamp(int(convert))
        except UnboundLocalError:
            return await ctx.send(f"`{date}` is not a valid timestamp.")
        curr = datetime.fromtimestamp(int(datetime.now().timestamp()))
        secs = str((curr - given).total_seconds())
        seconds = secs[1:][:-2] if "-" in secs else secs[:-2] if ".0" in secs else secs
        delta = humanize_timedelta(seconds=int(seconds))
        to = f"It will be in {delta}." if given > curr else f"It was {delta} ago."

        await ctx.send(f"Successfully converted `{date}` to `{convert}`\n{to}")

    @convert.command(aliases=["celsiustofahrenheit", "ctof", "celsiustokelvin", "ctok"])
    async def celsius(self, ctx, temperature: float):
        """
            Convert degree Celsius to Fahrenheit or Kelvin.

            Usage:
            To Fahrenheit: `[p]convert ctof`
            To Kelvin: `[p]convert ctok`
        """
        if not temperature:
            return await ctx.send_help()
        elif ctx.invoked_with in ["celsiustofahrenheit", "ctof"]:
            fahrenheit = round((temperature * 1.8) + 32, 1)
            msg = f"{temperature:,}° Celsius is equal to {fahrenheit:,}° Fahrenheit."
        elif ctx.invoked_with in ["celsiustokelvin", "ctok"]:
            kelvin = round((temperature + 273.15), 1)
            msg = f"{temperature:,}° Celsius is equal to {kelvin:,}° Kelvin."
        await ctx.send(msg)

    @convert.command(aliases=["fahrenheittocelsius", "ftoc", "fahrenheittokelvin", "ftok"])
    async def fahrenheit(self, ctx, temperature: float):
        """
            Convert Fahrenheit degree to Celsius or Kelvin.

            Usage:
            To Celsius: `[p]convert ftoc`
            To Kelvin: `[p]convert ftok`
        """
        if not temperature:
            return await ctx.send_help()
        elif ctx.invoked_with in ["fahrenheittocelsius", "ftoc"]:
            celsius = round((temperature - 32) / 1.8, 1)
            msg = f"{temperature:,}° Fahrenheit is equal to {celsius:,}° Celsius."
        elif ctx.invoked_with in ["fahrenheittokelvin", "ftok"]:
            kelvin = round((temperature - 32) * (5 / 9) + 273.15, 1)
            msg = f"{temperature:,}° Fahrenheit is equal to {kelvin:,}° Kelvin."
        await ctx.send(msg)

    @convert.command(aliases=["kelvintofahrenheit", "ktof", "kelvintocelsius", "ktoc"])
    async def kelvin(self, ctx, temperature: float):
        """
            Convert Kelvin degree to Fahrenheit or Celsius.

            Usage:
            To Fahrenheit: `[p]convert ktof`
            To Celsius: `[p]convert ktoc`
        """
        if not temperature:
            return await ctx.send_help()
        elif ctx.invoked_with in ["kelvintofahrenheit", "ktof"]:
            kelvin = round((temperature - 273.15) * (9 / 5) + 32, 1)
            msg = f"{temperature:,}° Kelvin is equal to {kelvin:,}° Fahrenheit."
        elif ctx.invoked_with in ["kelvintocelsius", "ktoc"]:
            kelvin = round((temperature - 273.15), 1)
            msg = f"{temperature:,}° Kelvin is equal to {kelvin:,}° Celsius."
        await ctx.send(msg)

    @convert.command(aliases=["lb"])
    async def pounds(self, ctx, mass: float):
        """Convert pounds to kilograms"""
        kg = round((mass * 0.45359237), 1)
        await ctx.send(f"{mass:,} lb is equal to {kg:,} kg.")

    @convert.command(aliases=["kg"])
    async def kilograms(self, ctx, mass: float):
        """Convert kilograms to pounds"""
        lb = round((mass / 0.45359237), 1)
        await ctx.send(f"{mass:,} kg is equal to {lb:,} lb.")
