from aiogram.types import InlineKeyboardButton

from src.bot.keyboards.buttons.post.post_buttons import PostActionButtons
from src.bot.keyboards.callback_data.streamer.post.post_cd import EditPostCD
from src.bot.keyboards.callback_data.streamer.post.post_media_cd import (
    GetPostMediaSessionCD,
)
from src.db.models.media_model import MediaSessionModel
from src.db.models.post_model import PostModel


def get_post_medias_back_button(post: PostModel, post_action_button: PostActionButtons):
    return InlineKeyboardButton(
        text="Назад",
        callback_data=EditPostCD.from_model(post.streamer, post_action_button).pack(),
    )


def get_post_media_back_button(post: PostModel, media_session: MediaSessionModel):
    return InlineKeyboardButton(
        text="Назад",
        callback_data=GetPostMediaSessionCD.from_model(post, media_session).pack(),
    )
