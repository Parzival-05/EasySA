import enum

from aiogram.types import KeyboardButton, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class MainMenuButtons(enum.StrEnum):
    STREAMERS = "Стримеры"
    MEDIAS = "Медиа"


def get_menu(message: Message):
    START_TEXT = (
        f"Привет, {message.from_user.first_name}! Ты стример и устал от рутины с уведомлением подписчиков о "
        f"стримах? Тогда этот бот для тебя! Бот предназначен для автоматического постинга уведомлений о "
        f"начале твоего прямого эфира в твоем личном канале/блоге.\n\n"
        f"На данный момент из стриминговых платформ поддерживаются Twitch. Из медиаплатформ — каналы в Telegram.\n\n"
        f'Быстрый старт: нажми на "{MainMenuButtons.STREAMERS.value}", добавь стримера, добавь нужное медиа, заполни '
        f"нужную информацию о посте в карточке стримера и активируй постинг!"
    )

    keyboard_build = ReplyKeyboardBuilder()
    keyboard_build.add(*[KeyboardButton(text=item) for item in MainMenuButtons])
    return message.reply(
        text=START_TEXT, reply_markup=keyboard_build.as_markup(resize_keyboard=True)
    )
