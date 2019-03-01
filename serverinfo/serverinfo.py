import discord

from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n

BaseCog = getattr(commands, "Cog", object)
_old_serverinfo = None
_ = Translator("ServerInfo", __file__)

@cog_i18n(_)
class ServerInfo(BaseCog):
    """
    Replace serverinfo command with more details.
    """
    
    __author__ = "Predä"

    def __init__(self, bot):
        self.bot = bot

    def __unload(self):
        global _old_serverinfo
        if _old_serverinfo:
            try:
                self.bot.remove_command("serverinfo")
            except:
                pass
            self.bot.add_command(_old_serverinfo)

    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """Show server information."""
        guild = ctx.guild

        def check_feature(feature):
            return "\N{WHITE HEAVY CHECK MARK}" if feature in guild.features else "\N{CROSS MARK}"

        format_kwargs = {
            "vip": check_feature("VIP_REGIONS"),
            "van": check_feature("VANITY_URL"),
            "splash": check_feature("INVITE_SPLASH"),
            "m_emojis": check_feature("MORE_EMOJI"),
            "verify": check_feature("VERIFIED"),
        }

        verif = {
            0: _("0 - None"),
            1: _("1 - Low"),
            2: _("2 - Medium"),
            3: _("3 - Hard"),
            4: _("4 - Extreme"),
        }
        region = {
            "vip-us-east": _("__VIP__ US East :flag_us:"),
            "vip-us-west": _("__VIP__ US West :flag_us:"),
            "vip-amsterdam": _("__VIP__ Amsterdam :flag_nl:"),
            "eu-west": _("EU West :flag_eu:"),
            "eu-central": _("EU Central :flag_eu:"),
            "london": _("London :flag_gb:"),
            "frankfurt": _("Frankfurt :flag_de:"),
            "amsterdam": _("Amsterdam :flag_nl:"),
            "us-west": _("US West :flag_us:"),
            "us-east": _("US East :flag_us:"),
            "us-south": _("US South :flag_us:"),
            "us-central": _("US Central :flag_us:"),
            "singapore": _("Singapore :flag_sg:"),
            "sydney": _("Sydney :flag_au:"),
            "brazil": _("Brazil :flag_br:"),
            "hongkong": _("Hong Kong :flag_hk:"),
            "russia": _("Russia :flag_ru:"),
            "japan": _("Japan :flag_jp:"),
            "southafrica": _("South Africa :flag_za:"),
        }
        online = len([m.status for m in guild.members if m.status == discord.Status.online])
        idle = len([m.status for m in guild.members if m.status == discord.Status.idle])
        dnd = len([m.status for m in guild.members if m.status == discord.Status.dnd])
        offline = len([m.status for m in guild.members if m.status == discord.Status.offline])
        streaming = len([m for m in guild.members if isinstance(m.activity, discord.Streaming)])
        mobile = len([m for m in guild.members if m.is_on_mobile()])
        lurkers = len([m for m in guild.members if m.joined_at is None])
        total_users = len(guild.members)
        humans = len([a for a in ctx.guild.members if a.bot == False])
        bots = len([a for a in ctx.guild.members if a.bot])
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        passed = (ctx.message.created_at - guild.created_at).days
        created_at = _("Created on **{date}**. That's over **{num}** days ago !").format(
            date=guild.created_at.strftime("%d %b %Y %H:%M"), num=passed
        )
        joined_at = guild.me.joined_at
        since_joined = (ctx.message.created_at - joined_at).days
        bot_joined = joined_at.strftime("%d %b %Y %H:%M:%S")
        joined_on = _(
            "{bot_name} joined this server on {bot_join}. That's over {since_join} days ago !"
        ).format(bot_name=ctx.bot.user.name, bot_join=bot_joined, since_join=since_joined)
        data = discord.Embed(description=created_at, colour=(await ctx.embed_colour()))
        if lurkers:
            data.add_field(
                name=_("Members :"),
                value=_(
                    "Total users : **{total}**\nLurkers : **{lurkers}**\nHumans : **{hum}** • Bots : **{bots}**\n"
                    "📗 `{online}` 📙 `{idle}`\n📕 `{dnd}` 📓 `{off}`\n"
                    "🎥 `{streaming}` 📱 `{mobile}`\n"
                ).format(
                    total=total_users,
                    lurkers=lurkers,
                    hum=humans,
                    bots=bots,
                    online=online,
                    idle=idle,
                    dnd=dnd,
                    off=offline,
                    streaming=streaming,
                    mobile=mobile,
                ),
            )
        else:
            data.add_field(
                name=_("Members :"),
                value=_(
                    "Total users : **{total}**\nHumans : **{hum}** • Bots : **{bots}**\n"
                    "📗 `{online}` 📙 `{idle}`\n📕 `{dnd}` 📓 `{off}`\n"
                    "🎥 `{streaming}` 📱 `{mobile}`\n"                    
                ).format(
                    total=total_users,
                    lurkers=lurkers,
                    hum=humans,
                    bots=bots,
                    online=online,
                    idle=idle,
                    dnd=dnd,
                    off=offline,
                    streaming=streaming,
                    mobile=mobile,
                ),
            )
        data.add_field(
            name=_("Channels :"),
            value=_("💬 Text : **{text}**\n🔊 Voice : **{voice}**").format(
                text=text_channels, voice=voice_channels
            ),
        )
        data.add_field(
            name=_("Utility :"),
            value=_(
                "Owner : **{owner}**\nRegion : **{region}**\nVerif. level : **{verif}**\nServer ID : **{id}**"
            ).format(
                owner=guild.owner,
                region=region[str(guild.region)],
                verif=verif[int(guild.verification_level)],
                id=guild.id,
            ),
        )
        data.add_field(
            name=_("Misc :"),
            value=_(
                "AFK channel : **{afk_chan}**\nAFK Timeout : **{afk_timeout}sec**\nCustom emojis : **{emojis}**\nRoles : **{roles}**"
            ).format(
                afk_chan=guild.afk_channel,
                afk_timeout=guild.afk_timeout,
                emojis=len(guild.emojis),
                roles=len(guild.roles),
            ),
        )
        if guild.features:
            data.add_field(
                name=_("Special features :"),
                value=_(
                    "{vip} VIP Regions\n{van} Vanity URL\n{splash} Splash Invite\n{m_emojis} More Emojis\n{verify} Verified"
                ).format(**format_kwargs),
            )
        data.set_author(name=guild.name)
        if "VERIFIED" in guild.features:
            data.set_author(
                name=guild.name,
                icon_url="https://cdn.discordapp.com/emojis/457879292152381443.png",
            )
        if guild.icon_url:
            data.set_thumbnail(url=guild.icon_url)
        else:
            data.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/494975386334134273/529843761635786754/Discord-Logo-Black.png"
            )
        data.set_footer(text=f"{joined_on}")

        try:
            await ctx.send(embed=data)
        except discord.Forbidden:
            await ctx.send(_("I need the `Embed links` permission to send this."))

def _unload(bot):
    bot.add_command("serverinfo")
        
def setup(bot):
    sinfo = ServerInfo(bot)
    global _old_serverinfo
    _old_serverinfo = bot.get_command("serverinfo")
    if _old_serverinfo:
        bot.remove_command(_old_serverinfo.name)
    bot.add_cog(sinfo)
