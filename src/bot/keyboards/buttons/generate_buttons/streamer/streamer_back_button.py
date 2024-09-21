from aiogram.types import InlineKeyboardButton

from src.bot.keyboards.buttons.streamer_buttons import StreamerInfoButtons
from src.bot.keyboards.callback_data.streamer.streamer_cd import GetStreamerCD
from src.db.models.streamer_model import StreamerModel


def get_streamer_back_button(streamer: StreamerModel):
    return InlineKeyboardButton(
        text="Назад",
        callback_data=GetStreamerCD.from_model(
            streamer, StreamerInfoButtons.STREAMER
        ).pack(),
    )
