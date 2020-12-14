import discord
from redbot.cogs.audio.audio_dataclasses import Query
from redbot.core import commands
from redbot.core.bot import Red


class Listeners:
    bot: Red
    cache: dict

    def upsert(self, key: str, value: int = 1):
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
            self.upsert("command_error")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            self.upsert("msg_sent")
        if message.guild is None:
            self.upsert("dms_received")
        self.upsert("messages_read")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.upsert("guild_join")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        self.upsert("guild_remove")

    @commands.Cog.listener()
    async def on_resumed(self):
        self.upsert("sessions_resumed")

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        self.upsert("processed_commands")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.upsert("new_members")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.upsert("members_left")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.upsert("messages_deleted")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        self.upsert("messages_edited")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        self.upsert("reactions_added")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        self.upsert("reactions_removed")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        self.upsert("roles_added")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        self.upsert("roles_removed")

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        self.upsert("roles_updated")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        self.upsert("members_banned")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        self.upsert("members_unbanned")

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        if len(before) > len(after):
            self.upsert("emojis_removed")
        elif len(before) < len(after):
            self.upsert("emojis_added")
        else:
            self.upsert("emojis_updated")

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member, before: discord.VoiceState, after: discord.VoiceState
    ):
        if not after.channel:
            return
        guild = after.channel.guild
        bot_in_room = guild.me in after.channel.members
        if bot_in_room:
            self.upsert("users_joined_bot_music_room")

    @commands.Cog.listener()
    async def on_red_audio_track_start(self, guild, track, requester):
        if not Query:
            return
        self.upsert("tracks_played")
        cog = self.bot.get_cog("Audio")
        query = Query.process_input(
            query=track.uri, _local_folder_current_path=cog.local_folder_current_path
        )
        if track.is_stream:
            self.upsert("streams_played")
        if track.is_stream and query.is_youtube:
            self.upsert("yt_streams_played")
        if track.is_stream and query.is_twitch:
            self.upsert("ttv_streams_played")
        if track.is_stream and query.is_other:
            self.upsert("other_streams_played")
        if query.is_youtube:
            self.upsert("youtube_tracks")
        if query.is_soundcloud:
            self.upsert("soundcloud_tracks")
        if query.is_bandcamp:
            self.upsert("bandcamp_tracks")
        if query.is_vimeo:
            self.upsert("vimeo_tracks")
        if query.is_twitch:
            self.upsert("twitch_tracks")
        if query.is_other:
            self.upsert("other_tracks")
