from typing import Type

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards.buttons.menu_buttons import BaseMenuButtons
from src.bot.keyboards.callback_data.menu_cd import MenuCD


def get_menu_buttons(menu_buttons: Type[BaseMenuButtons]):
    # noinspection PyTypeChecker
    return [
        InlineKeyboardButton(
            text=button, callback_data=MenuCD.from_button(button).pack()
        )
        for button in menu_buttons
    ]


def get_menu_buttons_markup(menu_buttons: Type[BaseMenuButtons]):
    keyboard_build = InlineKeyboardBuilder()
    keyboard_build.add(*get_menu_buttons(menu_buttons))
    return keyboard_build
