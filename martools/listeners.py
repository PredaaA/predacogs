import discord

from redbot.core import commands


class Listeners:
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error, unhandled_by_cog=False):
        if not unhandled_by_cog:
            if hasattr(ctx.command, "on_error"):
                return

            if ctx.cog:
                if commands.Cog._get_overridden_method(ctx.cog.cog_command_error) is not None:
                    return
        if isinstance(
            error,
            (
                commands.MissingRequiredArgument,
                commands.ConversionFailure,
                commands.UserInputError,
                commands.DisabledCommand,
                commands.CommandNotFound,
                commands.BotMissingPermissions,
                commands.UserFeedbackCheckFailure,
                commands.CheckFailure,
                commands.NoPrivateMessage,
                commands.CommandOnCooldown,
                getattr(commands, "ArgParserFailure", commands.UserInputError),
            ),
        ):
            return
        self.update_counters("command_error")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            self.update_counters("msg_sent")
        if message.guild is None:
            self.update_counters("dms_received")
        self.update_counters("messages_read")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.update_counters("guild_join")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        self.update_counters("guild_remove")

    @commands.Cog.listener()
    async def on_resumed(self):
        self.update_counters("sessions_resumed")

    @commands.Cog.listener()
    async def on_command(self, command):
        self.update_counters("processed_commands")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.update_counters("new_members")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.update_counters("members_left")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.update_counters("messages_deleted")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        self.update_counters("messages_edited")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        self.update_counters("reactions_added")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        self.update_counters("reactions_removed")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        self.update_counters("roles_added")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        self.update_counters("roles_removed")

    @commands.Cog.listener()
    async def on_guild_role_update(self, role):
        self.update_counters("roles_updated")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        self.update_counters("members_banned")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        self.update_counters("members_unbanned")

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        if len(before) > len(after):
            self.update_counters("emojis_removed")
        elif len(before) < len(after):
            self.update_counters("emojis_added")
        else:
            self.update_counters("emojis_updated")

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member, before: discord.VoiceState, after: discord.VoiceState
    ):
        if not after.channel:
            return
        guild = after.channel.guild
        bot_in_room = guild.me in after.channel.members
        if bot_in_room:
            self.update_counters("users_joined_bot_music_room")

    # @commands.Cog.listener()
    # async def on_red_audio_track_start(self, guild: discord.Guild, track, requester):
    #     self.update_counters("tracks_played")
    #     query = Query.process_input(track)
    #
    #     if track.is_stream:
    #         self.update_counters("streams_played")
    #         if query.is_youtube:
    #             self.update_counters("yt_streams_played")
    #         elif query.is_mixer:
    #             self.update_counters("mixer_streams_played")
    #         elif query.is_twitch:
    #             self.update_counters("ttv_streams_played")
    #         elif query.is_other:
    #             self.update_counters("other_streams_played")
    #
    #     if query.is_youtube:
    #         self.update_counters("youtube_tracks")
    #     elif query.is_soundcloud:
    #         self.update_counters("soundcloud_tracks")
    #     elif query.is_bandcamp:
    #         self.update_counters("bandcamp_tracks")
    #     elif query.is_vimeo:
    #         self.update_counters("vimeo_tracks")
    #     elif query.is_mixer:
    #         self.update_counters("mixer_tracks")
    #     elif query.is_twitch:
    #         self.update_counters("twitch_tracks")
    #     elif query.is_other:
    #         self.update_counters("other_tracks")
