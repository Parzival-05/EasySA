from aiogram.types import InlineKeyboardButton

from src.bot.keyboards.buttons.menu_buttons import MediaButtons
from src.bot.keyboards.callback_data.media.media_session_cd import GetMediaSessionCD
from src.bot.keyboards.callback_data.menu_cd import MenuCD
from src.db.models.media_model import MediaSessionModel


def get_media_sessions_back_button():
    return InlineKeyboardButton(
        text="Назад",
        callback_data=MenuCD.from_button(MediaButtons.GET_SESSIONS_LIST).pack(),
    )


def get_media_session_back_button(media_session: MediaSessionModel):
    return InlineKeyboardButton(
        text="Назад",
        callback_data=GetMediaSessionCD.from_model(media_session).pack(),
    )
