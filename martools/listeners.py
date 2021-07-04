import contextlib

import discord
from redbot.cogs.audio.audio_dataclasses import Query
from redbot.core import commands
from redbot.core.bot import Red


class Listeners:
    bot: Red
    cache: dict

    def upsert_cache(self, key: str, value: int = 1):
        with contextlib.suppress(AttributeError):
            self.cache["perma"][key] += value
            self.cache["session"][key] += value

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error, unhandled_by_cog=False):
        if not unhandled_by_cog:
            if hasattr(ctx.command, "on_error"):
                return

            if ctx.cog:
                if commands.Cog._get_overridden_method(ctx.cog.cog_command_error) is not None:
                    return
        if isinstance(error, commands.CommandInvokeError):
            self.upsert_cache("command_error")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            self.upsert_cache("msg_sent")
        if message.guild is None:
            self.upsert_cache("dms_received")
        self.upsert_cache("messages_read")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.upsert_cache("guild_join")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        self.upsert_cache("guild_remove")

    @commands.Cog.listener()
    async def on_resumed(self):
        self.upsert_cache("sessions_resumed")

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        self.upsert_cache("processed_commands")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.upsert_cache("new_members")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.upsert_cache("members_left")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.upsert_cache("messages_deleted")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        self.upsert_cache("messages_edited")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        self.upsert_cache("reactions_added")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        self.upsert_cache("reactions_removed")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        self.upsert_cache("roles_added")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        self.upsert_cache("roles_removed")

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        self.upsert_cache("roles_updated")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        self.upsert_cache("members_banned")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        self.upsert_cache("members_unbanned")

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        if len(before) > len(after):
            self.upsert_cache("emojis_removed")
        elif len(before) < len(after):
            self.upsert_cache("emojis_added")
        else:
            self.upsert_cache("emojis_updated")

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member, before: discord.VoiceState, after: discord.VoiceState
    ):
        if not after.channel:
            return
        guild = after.channel.guild
        bot_in_room = guild.me in after.channel.members
        if bot_in_room:
            self.upsert_cache("users_joined_bot_music_room")

    @commands.Cog.listener()
    async def on_red_audio_track_start(self, guild, track, requester):
        if not Query:
            return

        self.upsert_cache("tracks_played")
        if track.is_stream:
            self.upsert_cache("streams_played")

        cog = self.bot.get_cog("Audio")
        if cog:
            query = Query.process_input(
                query=track.uri, _local_folder_current_path=cog.local_folder_current_path
            )
            if track.is_stream and query.is_youtube:
                self.upsert_cache("yt_streams_played")
            if track.is_stream and query.is_twitch:
                self.upsert_cache("ttv_streams_played")
            if track.is_stream and query.is_other:
                self.upsert_cache("other_streams_played")
            if query.is_youtube:
                self.upsert_cache("youtube_tracks")
            if query.is_soundcloud:
                self.upsert_cache("soundcloud_tracks")
            if query.is_bandcamp:
                self.upsert_cache("bandcamp_tracks")
            if query.is_vimeo:
                self.upsert_cache("vimeo_tracks")
            if query.is_twitch:
                self.upsert_cache("twitch_tracks")
            if query.is_other:
                self.upsert_cache("other_tracks")
