import discord

from redbot.core import commands

from martools.utils import rgetattr

try:
    from redbot.cogs.audio.audio_dataclasses import Query
except ImportError:
    Query = None


class Listeners:
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error, unhandled_by_cog=False):
        if not unhandled_by_cog:
            if hasattr(ctx.command, "on_error"):
                return

            if ctx.cog:
                if commands.Cog._get_overridden_method(ctx.cog.cog_command_error) is not None:
                    return
        if isinstance(error, commands.CommandInvokeError):
            self.upset(rgetattr(ctx, "guild.id", rgetattr(ctx, "channel.id", -1)), "command_error")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            self.upset(rgetattr(message, "guild.id", -1), "msg_sent")
        if message.guild is None:
            self.upset(rgetattr(message, "channel.id", -1), "dms_received")
        self.upset(
            rgetattr(message, "guild.id", rgetattr(message, "channel.id", -1)), "messages_read"
        )

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.upset(rgetattr(guild, "id", -1), "guild_join")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        self.upset(rgetattr(guild, "id", -1), "guild_remove")

    @commands.Cog.listener()
    async def on_resumed(self):
        self.upset(0, "sessions_resumed")

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        self.upset(
            rgetattr(ctx, "guild.id", rgetattr(ctx, "channel.id", -1)), "processed_commands"
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.upset(rgetattr(member, "guild.id", -1), "new_members")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.upset(rgetattr(member, "guild.id", -1), "members_left")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.upset(
            rgetattr(message, "guild.id", rgetattr(message, "channel.id", -1)), "messages_deleted"
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        self.upset(
            rgetattr(after, "guild.id", rgetattr(after, "channel.id", -1)), "messages_edited"
        )

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        self.upset(rgetattr(user, "guild.id", user.id), "reactions_added")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        self.upset(rgetattr(user, "guild.id", user.id), "reactions_removed")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        self.upset(rgetattr(role.guild, "id", -1), "roles_added")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        self.upset(rgetattr(role.guild, "id", -1), "roles_removed")

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        self.upset(rgetattr(after.guild, "id", -1), "roles_updated")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        self.update_counters("members_banned")
        self.upset(rgetattr(guild, "id", -1), "members_unbanned")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        self.upset(rgetattr(guild, "id", -1), "members_unbanned")

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        if len(before) > len(after):
            self.upset(rgetattr(guild, "id", -1), "emojis_removed")
        elif len(before) < len(after):
            self.upset(rgetattr(guild, "id", -1), "emojis_added")
        else:
            self.upset(rgetattr(guild, "id", -1), "emojis_updated")

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member, before: discord.VoiceState, after: discord.VoiceState
    ):
        if not after.channel:
            return
        guild = after.channel.guild
        bot_in_room = guild.me in after.channel.members
        if bot_in_room:
            self.upset(rgetattr(member, "guild.id", -1), "users_joined_bot_music_room")

    @commands.Cog.listener()
    async def on_track_start(self, guild, track, requester):
        if not Query:
            return
        self.upset(rgetattr(guild, "id", -1), "tracks_played")
        query = Query.process_input(track.uri)
        if track.is_stream:
            self.upset(rgetattr(guild, "id", -1), "streams_played")
        if track.is_stream and query.is_youtube:
            self.upset(rgetattr(guild, "id", -1), "yt_streams_played")
        if track.is_stream and query.is_mixer:
            self.upset(rgetattr(guild, "id", -1), "mixer_streams_played")
        if track.is_stream and query.is_twitch:
            self.upset(rgetattr(guild, "id", -1), "ttv_streams_played")
        if track.is_stream and query.is_other:
            self.upset(rgetattr(guild, "id", -1), "other_streams_played")
        if query.is_youtube:
            self.upset(rgetattr(guild, "id", -1), "youtube_tracks")
        if query.is_soundcloud:
            self.upset(rgetattr(guild, "id", -1), "soundcloud_tracks")
        if query.is_bandcamp:
            self.upset(rgetattr(guild, "id", -1), "bandcamp_tracks")
        if query.is_vimeo:
            self.upset(rgetattr(guild, "id", -1), "vimeo_tracks")
        if query.is_mixer:
            self.upset(rgetattr(guild, "id", -1), "mixer_tracks")
        if query.is_twitch:
            self.upset(rgetattr(guild, "id", -1), "twitch_tracks")
        if query.is_other:
            self.upset(rgetattr(guild, "id", -1), "other_tracks")
