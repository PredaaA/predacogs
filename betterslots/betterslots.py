# Remove command logic are from : https://github.com/mikeshardmind/SinbadCogs/tree/v3/messagebox

import discord

from collections import deque
from enum import Enum
from typing import cast, Iterable, Sequence

from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core import Config, bank, commands, errors

from .miscs import guild_only_check, SMReel, PAYOUTS, SLOT_PAYOUTS_MSG

import asyncio
import calendar
import random

BaseCog = getattr(commands, "Cog", object)
_old_slots = None
T_ = Translator("BetterSlots", __file__)
_ = T_


@cog_i18n(_)
class BetterSlots(BaseCog):
    """
    Replace slots command with a new different one.
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(None, 1256844281, cog_name="economy")

    @commands.command(aliases=["slots"])
    @commands.bot_has_permissions(embed_links=True)
    @guild_only_check()
    async def slot(self, ctx: commands.Context, bid: int):
        """Use the slot machine."""
        author = ctx.author
        guild = ctx.guild
        channel = ctx.channel
        if await bank.is_global():
            valid_bid = await self.config.SLOT_MIN() <= bid <= await self.config.SLOT_MAX()
            slot_time = await self.config.SLOT_TIME()
            last_slot = await self.config.user(author).last_slot()
        else:
            valid_bid = (
                await self.config.guild(guild).SLOT_MIN()
                <= bid
                <= await self.config.guild(guild).SLOT_MAX()
            )
            slot_time = await self.config.guild(guild).SLOT_TIME()
            last_slot = await self.config.member(author).last_slot()
        now = calendar.timegm(ctx.message.created_at.utctimetuple())

        em = discord.Embed(color=0xAA0000)
        if (now - last_slot) < slot_time:
            try:
                await ctx.message.delete()
            except discord.Forbidden:
                pass
            em.title = _("⛔ You're on cooldown ! Try again in a bit.")
            await ctx.send(embed=em, delete_after=1)
            return
        if not valid_bid:
            em.title = _("⛔ That's an invalid bid amount, sorry.")
            await ctx.send(embed=em)
            return
        if not await bank.can_spend(author, bid):
            em.title = _("⛔ You ain't got enough money, friend.")
            await ctx.send(embed=em)
            return
        if await bank.is_global():
            await self.config.user(author).last_slot.set(now)
        else:
            await self.config.member(author).last_slot.set(now)
        await self.slot_machine(author, channel, bid, ctx)

    @staticmethod
    async def slot_machine(author, channel, bid, ctx):
        default_reel = deque(cast(Iterable, SMReel))
        reels_roll = []
        for i in range(3):
            default_reel.rotate(random.randint(-999, 999))  # weeeeee
            new_reel = deque(default_reel, maxlen=3)  # we need only 3 symbols
            reels_roll.append(new_reel)  # for each reel

        rows_roll = (
            (reels_roll[0][0], reels_roll[1][0], reels_roll[2][0]),
            (reels_roll[0][1], reels_roll[1][1], reels_roll[2][1]),
            (reels_roll[0][2], reels_roll[1][2], reels_roll[2][2]),
        )

        reels_slot = []
        for i in range(3):
            default_reel.rotate(random.randint(-999, 999))
            new_reel = deque(default_reel, maxlen=3)
            reels_slot.append(new_reel)
        rows_slot = (
            (reels_slot[0][0], reels_slot[1][0], reels_slot[2][0]),
            (reels_slot[0][1], reels_slot[1][1], reels_slot[2][1]),
            (reels_slot[0][2], reels_slot[1][2], reels_slot[2][2]),
        )

        roll = "__\n__"
        for i, row in enumerate(rows_roll):
            sign = " "
            if i == 1:
                sign = " **◄**"
            roll += "**║** {} **¦** {} **¦** {} **║**{}\n\n".format(*[c.value for c in row], sign)

        slot = " "  # Mobile friendly
        for i, row in enumerate(rows_slot):  # Let's build the slot to show
            sign = " "
            if i == 1:
                sign = " **◄**"
            slot += "**║** {} **¦** {} **¦** {} **║**{}\n\n".format(*[c.value for c in row], sign)

        payout = PAYOUTS.get(rows_slot[1])
        if not payout:
            # Checks for two-consecutive-symbols special rewards
            payout = PAYOUTS.get(
                (rows_slot[1][0], rows_slot[1][1]), PAYOUTS.get((rows_slot[1][1], rows_slot[1][2]))
            )
        if not payout:
            # Still nothing. Let's check for 3 generic same symbols
            # or 2 consecutive symbols
            has_three = rows_slot[1][0] == rows_slot[1][1] == rows_slot[1][2]
            has_two = (rows_slot[1][0] == rows_slot[1][1]) or (rows_slot[1][1] == rows_slot[1][2])
            if has_three:
                payout = PAYOUTS["3 symbols"]
            elif has_two:
                payout = PAYOUTS["2 symbols"]

        if payout:
            then = await bank.get_balance(author)
            pay = payout["payout"](bid)
            now = then - bid + pay
            try:
                await bank.set_balance(author, now)
            except errors.BalanceTooHigh as exc:
                await bank.set_balance(author, exc.max_balance)
                await channel.send(
                    _(
                        "You've reached the maximum amount of {currency}! "
                        "Please spend some more \N{GRIMACING FACE}\n{old_balance} -> {new_balance}!"
                    ).format(
                        currency=await bank.get_currency_name(getattr(channel, "guild", None)),
                        old_balance=then,
                        new_balance=exc.max_balance,
                    )
                )
                return
            phrase = T_(payout["phrase"])
        else:
            then = await bank.get_balance(author)
            await bank.withdraw_credits(author, bid)
            now = then - bid
            phrase = _("You didn't win anything !")
        em_roll = discord.Embed(color=0xD0AF15, title=_("Rolling ... 🎰"), description=f"{roll}")
        pos = await bank.get_leaderboard_position(author)
        credits_name = await bank.get_currency_name(ctx.guild)
        amount_ = now - then
        if amount_ < 0:
            em_slot = discord.Embed(color=0xB21515, description=f"{slot}")
            em_msg = discord.Embed(description=f"{author.mention}", color=0xB21515)
            em_msg.add_field(
                name=f"{phrase}",
                value=_(
                    "Your bid : **{amount} {credits_name}**\n(**{amount_} {credits_name}**)"
                ).format(amount=bid, credits_name=credits_name, amount_=amount_),
            )
        else:
            em_slot = discord.Embed(color=0x15A317, description=f"{slot}")
            em_msg = discord.Embed(description=f"{author.mention}", color=0x15A317)
            em_msg.add_field(
                name=f"{phrase}",
                value=_(
                    "Your bid : **{amount} {credits_name}**\n(**+{amount_} {credits_name}**)"
                ).format(amount=bid, credits_name=credits_name, amount_=amount_),
            )
        em_msg.add_field(
            name=_("Balance :"),
            value=_(
                "Old balance : **{old_balance} {credits_name}**\nNew balance : **{new_balance} {credits_name}**"
            ).format(credits_name=credits_name, old_balance=then, new_balance=now),
            inline=False,
        )
        footer = _("You are #{pos} on the {scope}leaderboard!").format(
            pos=pos, scope="global " if await bank.is_global() else ""
        )
        em_msg.set_footer(text=footer)
        slots = await channel.send(embed=em_roll)
        await asyncio.sleep(0.3)
        await slots.edit(embed=em_slot)
        await channel.send(embed=em_msg)


async def _unload(ctx, bot):
    bot.add_command("slot")


def setup(bot):
    bslots = BetterSlots(bot)
    global _old_slots
    _old_slots = bot.get_command("slot")
    if _old_slots:
        bot.remove_command(_old_slots.name)
    bot.add_cog(bslots)
