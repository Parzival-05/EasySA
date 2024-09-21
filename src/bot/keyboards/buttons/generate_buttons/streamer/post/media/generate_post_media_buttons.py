from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards.buttons.post.media.post_media_buttons import (
    PostMediaActionButtons,
)
from src.bot.keyboards.callback_data.streamer.post.post_media_cd import (
    GetPostMediaSessionCD,
    EditPostMediaSessionCD,
)
from src.db.models.association.post_media import PostMediaSessionJoin
from src.db.models.media_model import MediaSessionModel
from src.db.models.post_model import PostModel


def generate_post_media_session_text(
    media_session: MediaSessionModel,
    post_media_session_join: PostMediaSessionJoin,
):
    activity_status = (
        "🟢 Активен" if post_media_session_join.is_active else "🔴 Не активен"
    )
    return (
        f"{media_session.name} | {media_session.media_name.value} | {activity_status}"
    )


def get_post_media_session_join(
    post_media_session_joins: list[PostMediaSessionJoin],
    media_session: MediaSessionModel,
):
    for post_media_session_join in post_media_session_joins:
        if post_media_session_join.media_session_id == media_session.id:
            return post_media_session_join


async def get_post_media_sessions_inline_keyboard(
    post: PostModel,
    post_media_session_joins: list[PostMediaSessionJoin],
    media_sessions: list[MediaSessionModel],
):
    keyboard_build = InlineKeyboardBuilder()
    for media_session in media_sessions:
        keyboard_build.button(
            text=generate_post_media_session_text(
                media_session,
                get_post_media_session_join(post_media_session_joins, media_session),
            ),
            callback_data=GetPostMediaSessionCD.from_model(post, media_session),
        )
    return keyboard_build.adjust(1)


async def get_post_media_session_actions_inline_keyboard(
    post: PostModel,
    media_session: MediaSessionModel,
    post_media_session_join: PostMediaSessionJoin,
):
    action_buttons: list[PostMediaActionButtons] = [
        (
            PostMediaActionButtons.SET_AS_INACTIVE
            if post_media_session_join.is_active
            else PostMediaActionButtons.SET_AS_ACTIVE
        )
    ]
    keyboard_build = InlineKeyboardBuilder()
    for action_button in action_buttons:
        keyboard_build.button(
            text=action_button,
            callback_data=EditPostMediaSessionCD.from_model(
                post, media_session, action_button
            ),
        )
    return keyboard_build.adjust(1)
