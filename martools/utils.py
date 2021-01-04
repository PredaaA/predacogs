from concurrent.futures._base import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List

events_names = (
    "on_error",
    "msg_sent",
    "dms_received",
    "messages_read",
    "guild_join",
    "guild_remove",
    "sessions_resumed",
    "processed_commands",
    "new_members",
    "members_left",
    "messages_deleted",
    "messages_edited",
    "reactions_added",
    "reactions_removed",
    "roles_added",
    "roles_removed",
    "roles_updated",
    "members_banned",
    "members_unbanned",
    "emojis_removed",
    "emojis_added",
    "emojis_updated",
    "users_joined_bot_music_room",
    "tracks_played",
    "streams_played",
    "yt_streams_played",
    "mixer_streams_played",
    "ttv_streams_played",
    "other_streams_played",
    "youtube_tracks",
    "soundcloud_tracks",
    "bandcamp_tracks",
    "vimeo_tracks",
    "mixer_tracks",
    "twitch_tracks",
    "other_tracks",
)


def threadexec(func, *args) -> List:
    result = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        for future in as_completed([executor.submit(func, *args)]):
            result = future.result()
    return result
