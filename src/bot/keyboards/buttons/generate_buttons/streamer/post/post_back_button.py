from aiogram.types import InlineKeyboardButton

from src.bot.keyboards.buttons.streamer_buttons import StreamerInfoButtons
from src.bot.keyboards.callback_data.streamer.post.post_cd import GetPostCD
from src.bot.keyboards.callback_data.streamer.streamer_cd import GetStreamerCD
from src.db.models.post_model import PostModel
from src.db.models.streamer_model import StreamerModel


def get_posts_back_button(streamer: StreamerModel):
    return InlineKeyboardButton(
        text="Назад",
        callback_data=GetStreamerCD.from_model(
            streamer, StreamerInfoButtons.POSTS
        ).pack(),
    )


def get_post_back_button(post: PostModel):
    return InlineKeyboardButton(
        text="Назад",
        callback_data=GetPostCD.from_model(post).pack(),
    )
