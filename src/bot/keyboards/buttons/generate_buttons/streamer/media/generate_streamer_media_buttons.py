from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards.callback_data.streamer.media.streamer_media_cd import (
    GetStreamerMediaSessionCD,
    AddStreamerMediaSessionCD,
)
from src.db.models.association.streamer_media_session import StreamerMediaSessionJoin
from src.db.models.media_model import MediaSessionModel
from src.db.models.streamer_model import StreamerModel


def generate_media_session_text_for_get(
    media_session: MediaSessionModel,
    streamer_media_session_join: StreamerMediaSessionJoin,
):
    activity_status = (
        "🟢 Постинг активен"
        if streamer_media_session_join.is_active
        else "🔴 Постинг не активен"
    )
    return (
        f"{media_session.name} | {media_session.media_name.value} | {activity_status}"
    )


def generate_media_session_text_for_add(
    media_session: MediaSessionModel,
):
    return f"{media_session.name} | {media_session.media_name.value}"


def get_streamer_media_session_join(
    streamer_media_sessions_join: list[StreamerMediaSessionJoin],
    media_session: MediaSessionModel,
):
    for streamer_media_session_join in streamer_media_sessions_join:
        if streamer_media_session_join.media_session_id == media_session.id:
            return streamer_media_session_join


async def get_streamer_media_sessions_inline_keyboard(
    streamer: StreamerModel,
    streamer_media_sessions_join: list[StreamerMediaSessionJoin],
):
    media_sessions = streamer.media_sessions
    keyboard_build = InlineKeyboardBuilder()
    for media_session in media_sessions:
        keyboard_build.button(
            text=generate_media_session_text_for_get(
                media_session,
                get_streamer_media_session_join(
                    streamer_media_sessions_join, media_session
                ),
            ),
            callback_data=GetStreamerMediaSessionCD.from_model(media_session, streamer),
        )
    return keyboard_build.adjust(1)


async def get_available_for_streamer_media_sessions_inline_keyboard(
    streamer: StreamerModel,
    streamer_media_sessions_join: list[StreamerMediaSessionJoin],
    media_sessions: list[MediaSessionModel],
):
    keyboard_build = InlineKeyboardBuilder()
    for media_session in media_sessions:
        streamer_media_session_join = get_streamer_media_session_join(
            streamer_media_sessions_join, media_session
        )
        if not streamer_media_session_join:
            keyboard_build.button(
                text=generate_media_session_text_for_add(media_session),
                callback_data=AddStreamerMediaSessionCD.from_model(
                    media_session, streamer
                ),
            )
    return keyboard_build.adjust(1)
