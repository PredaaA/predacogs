import discord

from redbot.core import commands, bank
from enum import Enum


def guild_only_check():
    async def pred(ctx: commands.Context):
        if await bank.is_global():
            return True
        elif not await bank.is_global() and ctx.guild is not None:
            return True
        else:
            return False

    return commands.check(pred)


NUM_ENC = "\N{COMBINING ENCLOSING KEYCAP}"


class SMReel(Enum):
    cherries = "\N{CHERRIES}"
    cookie = "\N{COOKIE}"
    two = "\N{DIGIT TWO}" + NUM_ENC
    flc = "\N{FOUR LEAF CLOVER}"
    cyclone = "\N{CYCLONE}"
    sunflower = "\N{SUNFLOWER}"
    six = "\N{DIGIT SIX}" + NUM_ENC
    mushroom = "\N{MUSHROOM}"
    heart = "\N{HEAVY BLACK HEART}"
    snowflake = "\N{SNOWFLAKE}"


_ = lambda s: s
PAYOUTS = {
    (SMReel.two, SMReel.two, SMReel.six): {
        "payout": lambda x: x * 2500 + x,
        "phrase": _("JACKPOT ! :two: :two: :six: ! 🎉 🍾\nYour bid has been multiplied x2500 !"),
    },
    (SMReel.flc, SMReel.flc, SMReel.flc): {
        "payout": lambda x: x + 1000,
        "phrase": _("3 🍀 ! +1000 !"),
    },
    (SMReel.cherries, SMReel.cherries, SMReel.cherries): {
        "payout": lambda x: x + 800,
        "phrase": _("Three cherries 🍒🍒🍒 ! +800 !"),
    },
    (SMReel.two, SMReel.six): {
        "payout": lambda x: x * 4 + x,
        "phrase": _(":two: :six: ! Your bid has been multiplied x4 !"),
    },
    (SMReel.cherries, SMReel.cherries): {
        "payout": lambda x: x * 3 + x,
        "phrase": _("Two cherries ! 🍒🍒\nYour bid has been multiplied x3 !"),
    },
    "3 symbols": {"payout": lambda x: x + 500, "phrase": _("Three symbols ! +500 !")},
    "2 symbols": {
        "payout": lambda x: x * 2 + x,
        "phrase": _("Two consecutive symbols ! 🎉\nYour bid has been multiplied x2 !"),
    },
}

SLOT_PAYOUTS_MSG = discord.Embed(
    color=0x10A714,
    description=_(
        "**Slot machine payouts :**\n\n"
        "{two.value} {two.value} {six.value} Bet **x2500**\n"
        "{flc.value} {flc.value} {flc.value} **+1000**\n"
        "{cherries.value} {cherries.value} {cherries.value} **+800**\n"
        "{two.value} {six.value} **Bet x4**\n"
        "{cherries.value} {cherries.value} **Bet x3**\n\n"
        "Three symbols: **+500**\n"
        "Two symbols: **Bet x2**"
    ).format(**SMReel.__dict__),
)
