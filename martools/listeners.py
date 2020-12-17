import discord
from redbot.core.bot import Red
from redbot.core import commands
from redbot.core.data_manager import cog_data_path

import apsw
import time

from .utils import rgetattr, threadexec
from .statements import (
    PRAGMA_journal_mode,
    PRAGMA_wal_autocheckpoint,
    # PRAGMA_read_uncommitted,
    CREATE_TABLE_PERMA,
    DROP_TEMP,
    CREATE_TABLE_TEMP,
    INSERT_PERMA_DO_NOTHING,
    UPSERT_PERMA,
    UPSERT_TEMP,
)

try:
    from redbot.cogs.audio.audio_dataclasses import Query
except ImportError:
    Query = None


class Listeners:
    def __init__(self):
        self.bot: Red

        self._connection = apsw.Connection(str(cog_data_path(self) / "MartTools.db"))
        self.cursor = self._connection.cursor()

        threadexec(self.cursor.execute, PRAGMA_journal_mode)
        threadexec(self.cursor.execute, PRAGMA_wal_autocheckpoint)
        threadexec(self.cursor.execute, CREATE_TABLE_PERMA)
        threadexec(self.cursor.execute, DROP_TEMP)
        threadexec(self.cursor.execute, CREATE_TABLE_TEMP)
        threadexec(
            self.cursor.execute, INSERT_PERMA_DO_NOTHING, (-1000, "creation_time", time.time())
        )

    def upsert(self, id: int, event: str):
        threadexec(self.cursor.execute, UPSERT_PERMA, (id, event))
        threadexec(self.cursor.execute, UPSERT_TEMP, (id, event))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error, unhandled_by_cog=False):
        if not unhandled_by_cog:
            if hasattr(ctx.command, "on_error"):
                return

            if ctx.cog:
                if commands.Cog._get_overridden_method(ctx.cog.cog_command_error) is not None:
                    return
        if isinstance(error, commands.CommandInvokeError):
            self.upsert(
                rgetattr(ctx, "guild.id", rgetattr(ctx, "channel.id", -1)), "command_error"
            )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            self.upsert(rgetattr(message, "guild.id", -1), "msg_sent")
        if message.guild is None:
            self.upsert(rgetattr(message, "channel.id", -1), "dms_received")
        self.upsert(
            rgetattr(message, "guild.id", rgetattr(message, "channel.id", -1)), "messages_read"
        )

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.upsert(rgetattr(guild, "id", -1), "guild_join")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        self.upsert(rgetattr(guild, "id", -1), "guild_remove")

    @commands.Cog.listener()
    async def on_resumed(self):
        self.upsert(0, "sessions_resumed")

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        self.upsert(
            rgetattr(ctx, "guild.id", rgetattr(ctx, "channel.id", -1)), "processed_commands"
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.upsert(rgetattr(member, "guild.id", -1), "new_members")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.upsert(rgetattr(member, "guild.id", -1), "members_left")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.upsert(
            rgetattr(message, "guild.id", rgetattr(message, "channel.id", -1)), "messages_deleted"
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        self.upsert(
            rgetattr(after, "guild.id", rgetattr(after, "channel.id", -1)), "messages_edited"
        )

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        self.upsert(rgetattr(user, "guild.id", user.id), "reactions_added")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        self.upsert(rgetattr(user, "guild.id", user.id), "reactions_removed")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        self.upsert(rgetattr(role.guild, "id", -1), "roles_added")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        self.upsert(rgetattr(role.guild, "id", -1), "roles_removed")

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        self.upsert(rgetattr(after.guild, "id", -1), "roles_updated")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        self.upsert(rgetattr(guild, "id", -1), "members_banned")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        self.upsert(rgetattr(guild, "id", -1), "members_unbanned")

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        if len(before) > len(after):
            self.upsert(rgetattr(guild, "id", -1), "emojis_removed")
        elif len(before) < len(after):
            self.upsert(rgetattr(guild, "id", -1), "emojis_added")
        else:
            self.upsert(rgetattr(guild, "id", -1), "emojis_updated")

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member, before: discord.VoiceState, after: discord.VoiceState
    ):
        if not after.channel:
            return
        guild = after.channel.guild
        bot_in_room = guild.me in after.channel.members
        if bot_in_room:
            self.upsert(rgetattr(member, "guild.id", -1), "users_joined_bot_music_room")

    @commands.Cog.listener()
    async def on_red_audio_track_start(self, guild, track, requester):
        if not Query:
            return
        self.upsert(rgetattr(guild, "id", -1), "tracks_played")
        cog = self.bot.get_cog("Audio")
        if hasattr(cog, "local_folder_current_path"):
            query = Query.process_input(
                query=track.uri, _local_folder_current_path=cog.local_folder_current_path
            )
        else:
            query = Query.process_input(query=track.uri)
        if track.is_stream:
            self.upsert(rgetattr(guild, "id", -1), "streams_played")
        if track.is_stream and query.is_youtube:
            self.upsert(rgetattr(guild, "id", -1), "yt_streams_played")
        if track.is_stream and query.is_mixer:
            self.upsert(rgetattr(guild, "id", -1), "mixer_streams_played")
        if track.is_stream and query.is_twitch:
            self.upsert(rgetattr(guild, "id", -1), "ttv_streams_played")
        if track.is_stream and query.is_other:
            self.upsert(rgetattr(guild, "id", -1), "other_streams_played")
        if query.is_youtube:
            self.upsert(rgetattr(guild, "id", -1), "youtube_tracks")
        if query.is_soundcloud:
            self.upsert(rgetattr(guild, "id", -1), "soundcloud_tracks")
        if query.is_bandcamp:
            self.upsert(rgetattr(guild, "id", -1), "bandcamp_tracks")
        if query.is_vimeo:
            self.upsert(rgetattr(guild, "id", -1), "vimeo_tracks")
        if query.is_mixer:
            self.upsert(rgetattr(guild, "id", -1), "mixer_tracks")
        if query.is_twitch:
            self.upsert(rgetattr(guild, "id", -1), "twitch_tracks")
        if query.is_other:
            self.upsert(rgetattr(guild, "id", -1), "other_tracks")
