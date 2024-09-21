from aiogram.types import InlineKeyboardButton

from src.bot.keyboards.buttons.menu_buttons import BaseMenuButtons
from src.bot.keyboards.callback_data.menu_cd import MenuCD


def get_menu_back_button(button: BaseMenuButtons):
    return InlineKeyboardButton(
        text="Назад",
        callback_data=MenuCD.from_button(button).pack(),
    )
