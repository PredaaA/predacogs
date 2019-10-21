import discord

from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import (
    bold,
    humanize_timedelta,
)  # , humanize_number <- Will be for 3.2

from typing import Union  # <- Remove this at 3.2
from babel.numbers import format_decimal  # <- Remove this at 3.2

_old_serverinfo = None
_ = Translator("ServerInfo", __file__)


def humanize_number(val: Union[int, float]):  # <- Remove this at 3.2
    return format_decimal(val, locale="en_US")


@cog_i18n(_)
class ServerInfo(commands.Cog):
    """Replace original Red serverinfo command with more details."""

    __author__ = "Predä"
    __version__ = "1.2.4"

    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        # Remove command logic are from: https://github.com/mikeshardmind/SinbadCogs/tree/v3/messagebox
        global _old_serverinfo
        if _old_serverinfo:
            try:
                self.bot.remove_command("serverinfo")
            except Exception as error:
                print(error)
            self.bot.add_command(_old_serverinfo)

    @staticmethod
    def _size(num):
        for unit in ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
            if abs(num) < 1024.0:
                return "{0:.1f}{1}".format(num, unit)
            num /= 1024.0
        return "{0:.1f}{1}".format(num, "YB")

    @staticmethod
    def _bitsize(num):
        for unit in ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
            if abs(num) < 1000.0:
                return "{0:.1f}{1}".format(num, unit)
            num /= 1000.0
        return "{0:.1f}{1}".format(num, "YB")

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    async def serverinfo(self, ctx):
        """Show server information with some details."""
        guild = ctx.guild
        passed = (ctx.message.created_at - guild.created_at).days
        created_at = _("Created on {date}. That's over {num} days ago!").format(
            date=bold(guild.created_at.strftime("%d %b %Y %H:%M")),
            num=bold(humanize_number(passed)),
        )

        # Logic from: https://github.com/TrustyJAID/Trusty-cogs/blob/master/serverstats/serverstats.py#L159
        lurkers_len = len([m for m in guild.members if m.joined_at is None])
        online_stats = {
            _("Humans: "): lambda x: not x.bot,
            _(" • Bots: "): lambda x: x.bot,
            "📗": lambda x: x.status == discord.Status.online,
            "📙": lambda x: x.status == discord.Status.idle,
            "📕": lambda x: x.status == discord.Status.idle,
            "📓": lambda x: x.status == discord.Status.offline,
            "🎥": lambda x: x.activity == discord.Streaming,
            "📱": lambda x: x.is_on_mobile(),
        }
        member_msg = _("Total Users: {total}\n").format(
            total=bold(humanize_number(guild.member_count))
        )
        member_msg += (
            _("Lurkers: {lurkers}").format(lurkers=bold(humanize_number(lurkers_len)))
            if lurkers_len
            else ""
        )
        count = 1
        for emoji, value in online_stats.items():
            try:
                num = len([m for m in guild.members if value(m)])
            except Exception as error:
                print(error)
                continue
            else:
                member_msg += f"{emoji} {bold(humanize_number(num))} " + (
                    "\n" if count % 2 == 0 else ""
                )
            count += 1

        text_channels = len(guild.text_channels)
        nsfw_channels = len([c for c in guild.text_channels if c.is_nsfw()])
        voice_channels = len(guild.voice_channels)

        vc_regions = {
            "vip-us-east": _("__VIP__ US East ") + "\U0001F1FA\U0001F1F8",
            "vip-us-west": _("__VIP__ US West ") + "\U0001F1FA\U0001F1F8",
            "vip-amsterdam": _("__VIP__ Amsterdam ") + "\U0001F1F3\U0001F1F1",
            "eu-west": _("EU West ") + "\U0001F1EA\U0001F1FA",
            "eu-central": _("EU Central ") + "\U0001F1EA\U0001F1FA",
            "europe": _("Europe ") + "\U0001F1EA\U0001F1FA",
            "london": _("London ") + "\U0001F1EC\U0001F1E7",
            "frankfurt": _("Frankfurt ") + "\U0001F1E9\U0001F1EA",
            "amsterdam": _("Amsterdam ") + "\U0001F1F3\U0001F1F1",
            "us-west": _("US West ") + "\U0001F1FA\U0001F1F8",
            "us-east": _("US East ") + "\U0001F1FA\U0001F1F8",
            "us-south": _("US South ") + "\U0001F1FA\U0001F1F8",
            "us-central": _("US Central ") + "\U0001F1FA\U0001F1F8",
            "singapore": _("Singapore ") + "\U0001F1F8\U0001F1EC",
            "sydney": _("Sydney ") + "\U0001F1E6\U0001F1FA",
            "brazil": _("Brazil ") + "\U0001F1E7\U0001F1F7",
            "hongkong": _("Hong Kong ") + "\U0001F1ED\U0001F1F0",
            "russia": _("Russia ") + "\U0001F1F7\U0001F1FA",
            "japan": _("Japan ") + "\U0001F1EF\U0001F1F5",
            "southafrica": _("South Africa ") + "\U0001F1FF\U0001F1E6",
            "india": _("India ") + "\U0001F1EE\U0001F1F3",
        }  # Unicode is needed because bold() is escaping emojis for some reason in this case.
        verif = {
            "none": _("0 - None"),
            "low": _("1 - Low"),
            "medium": _("2 - Medium"),
            "high": _("3 - Hard"),
            "extreme": _("4 - Extreme"),
        }

        features = {
            "PARTNERED": _("Partnered"),
            "VERIFIED": _("Verified"),
            "DISCOVERABLE": _("Server Discovery"),
            "PUBLIC": _("Public"),
            "INVITE_SPLASH": _("Splash Invite"),
            "VIP_REGIONS": _("VIP Voice Servers"),
            "VANITY_URL": _("Vanity URL"),
            "MORE_EMOJI": _("More Emojis"),
            "COMMERCE": _("Commerce"),
            "LURKABLE": _("Lurkable"),
            "NEWS": _("News Channels"),
            "ANIMATED_ICON": _("Animated Icon"),
            "BANNER": _("Banner Image"),
            "MEMBER_LIST_DISABLED": _("Member list disabled"),
        }
        guild_features_list = [
            f"`\N{WHITE HEAVY CHECK MARK}` {name}"
            for feature, name in features.items()
            if feature in set(guild.features)
        ]

        since_joined = (ctx.message.created_at - guild.me.joined_at).days
        bot_joined = guild.me.joined_at.strftime("%d %b %Y %H:%M:%S")
        joined_on = _(
            "{bot_name} joined this server on {bot_join}. That's over {since_join} days ago!"
        ).format(
            bot_name=self.bot.user.name,
            bot_join=bot_joined,
            since_join=humanize_number(since_joined),
        )

        em = discord.Embed(description=created_at, colour=await ctx.embed_colour())
        em.set_author(
            name=guild.name,
            icon_url="https://cdn.discordapp.com/emojis/457879292152381443.png"
            if "VERIFIED" in guild.features
            else "https://cdn.discordapp.com/emojis/508929941610430464.png"
            if "PARTNERED" in guild.features
            else discord.Embed.Empty,
        )
        em.set_thumbnail(
            url=guild.icon_url
            if guild.icon_url
            else "https://cdn.discordapp.com/embed/avatars/1.png"
        )
        em.add_field(name=_("Members:"), value=member_msg)
        em.add_field(
            name=_("Channels:"),
            value=_(
                "\N{SPEECH BALLOON} Text: {text}\n{nsfw}"
                "\N{SPEAKER WITH THREE SOUND WAVES} Voice: {voice}"
            ).format(
                text=bold(humanize_number(text_channels)),
                nsfw=_("\N{NO ONE UNDER EIGHTEEN SYMBOL} Nsfw: {}\n").format(
                    bold(humanize_number(nsfw_channels))
                )
                if nsfw_channels
                else "",
                voice=bold(humanize_number(voice_channels)),
            ),
        )
        em.add_field(
            name=_("Utility:"),
            value=_(
                "Owner: {owner}\nRegion: {region}\nVerif. level: {verif}\nServer ID: {id}"
            ).format(
                owner=bold(str(guild.owner)),
                region=bold(vc_regions[str(guild.region)]),
                verif=bold(verif[str(guild.verification_level)]),
                id=bold(str(guild.id)),
            ),
        )
        em.add_field(
            name=_("Misc:"),
            value=_(
                "AFK channel: {afk_chan}\nAFK Timeout: {afk_timeout}\nCustom emojis: {emojis}\nRoles: {roles}"
            ).format(
                afk_chan=bold(str(guild.afk_channel)) if guild.afk_channel else bold(_("Not set")),
                afk_timeout=bold(humanize_timedelta(seconds=guild.afk_timeout)),
                emojis=bold(humanize_number(len(guild.emojis))),
                roles=bold(humanize_number(len(guild.roles))),
            ),
        )
        if guild_features_list:
            em.add_field(name=_("Server features:"), value="\n".join(guild_features_list))
        if guild.premium_tier != 0:
            nitro_boost = _(
                "Tier {boostlevel} with {nitroboosters} boosters\n"
                "File size limit: {filelimit}\n"
                "Emoji limit: {emojis_limit}\n"
                "VCs max bitrate: {bitrate}"
            ).format(
                boostlevel=bold(str(guild.premium_tier)),
                nitroboosters=bold(humanize_number(guild.premium_subscription_count)),
                filelimit=bold(self._size(guild.filesize_limit)),
                emojis_limit=bold(str(guild.emoji_limit)),
                bitrate=bold(self._bitsize(guild.bitrate_limit)),
            )
            em.add_field(name=_("Nitro Boost:"), value=nitro_boost)
        em.set_footer(text=joined_on)
        await ctx.send(embed=em)


def cog_unload(self):
    self.bot.add_command("serverinfo")


def setup(bot):
    sinfo = ServerInfo(bot)
    global _old_serverinfo
    _old_serverinfo = bot.get_command("serverinfo")
    if _old_serverinfo:
        bot.remove_command(_old_serverinfo.name)
    bot.add_cog(sinfo)
