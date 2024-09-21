from typing import Type

from aiogram import Router, F
from aiogram.types import Message

from src.bot.keyboards.buttons.generate_buttons.generate_menu_buttons import (
    get_menu_buttons_markup,
)
from src.bot.keyboards.buttons.menu_buttons import (
    MediaButtons,
    StreamerButtons,
    BaseMenuButtons,
)
from src.bot.keyboards.main_menu import MainMenuButtons

menu_router = Router()


# noinspection PyUnresolvedReferences
@menu_router.message(F.text.in_([item.value for item in MainMenuButtons]))
async def get_buttons(message: Message):
    def map_menu_items_to_buttons(item: MainMenuButtons) -> Type[BaseMenuButtons]:
        match item:
            case MainMenuButtons.STREAMERS:
                result = StreamerButtons
            case MainMenuButtons.MEDIAS:
                result = MediaButtons
            case _:
                raise RuntimeError("Unhandled menu button")
        return result

    text = MainMenuButtons(message.text)
    await message.answer(
        text="Выберите действие",
        reply_markup=get_menu_buttons_markup(map_menu_items_to_buttons(text)).as_markup(
            resize_keyboard=True
        ),
    )
