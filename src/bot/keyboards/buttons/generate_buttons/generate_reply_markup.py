import logging
from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_reply_markup(
    keyboard_builder: Optional[InlineKeyboardBuilder], *include_buttons
):
    keyboard_builder = (
        InlineKeyboardBuilder() if keyboard_builder is None else keyboard_builder
    )
    new_keyboard_builder = InlineKeyboardBuilder()
    for button in include_buttons:
        logging.debug(button)
        if button is not None:
            new_keyboard_builder.add(button)

    return keyboard_builder.attach(new_keyboard_builder.adjust(1)).as_markup(
        resize_keyboard=True
    )
