import logging
from typing import Optional

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.actor.base_media_actor import BaseMediaActor
from src.checker.post_info import PostVariables
from src.db.models.post_model import ButtonsInfoModel
from src.domain.media_platforms.buttons import ButtonsParser, Button
from src.domain.stream_platforms.get_by_name import get_stream_platform_profile_class
from src.domain.stream_platforms.profiles.base_stream_profile import StreamProfileInfo


async def generate_buttons_markup(buttons_info: ButtonsInfoModel) -> InlineKeyboardMarkup:
    buttons = await ButtonsParser(buttons_info.buttons_info).parse()

    def map_to_inline_keyboard_button(button: Button) -> InlineKeyboardButton:
        return InlineKeyboardButton(text=button.text, url=button.url)

    def map_row_to_inline_keyboard_button_row(row: list[Button]) -> list[InlineKeyboardButton]:
        return list(map(map_to_inline_keyboard_button, row))

    keyboard_builder = InlineKeyboardBuilder(list(map(map_row_to_inline_keyboard_button_row, buttons)))
    return keyboard_builder.as_markup(resize_keyboard=True)


class TelegramActor(BaseMediaActor):
    CHAT_ID_TYPE = int

    def get_chat_id(self) -> Optional[CHAT_ID_TYPE]:
        return "@" + self.media_session.extra_field

    def _get_text(self):
        stream_platform_profile_class = get_stream_platform_profile_class(
            self.streamer.stream_platform_name
        )
        d = {
            PostVariables.STREAMER_URL.value.var: stream_platform_profile_class.generate_profile_url(
                StreamProfileInfo(profile_id=self.streamer.profile_id)
            ),
            PostVariables.STREAM_TITLE.value.var: self.stream_info.title,
            PostVariables.STREAM_CATEGORY.value.var: self.stream_info.category,
        }
        return self.post.text.format(**d)

    async def _send_post(
            self, chat_id: CHAT_ID_TYPE, text: str, buttons_info: ButtonsInfoModel, photo: Optional[str] = None,
            **kwargs
    ):
        ESCAPE_CHARS = [
            ".",
            "_",
            "*",
            "[",
            "]",
            "(",
            ")",
            "~",
            "`",
            ">",
            "#",
            "+",
            "-",
            "=",
            "|",
            "{",
            "}",
            "!",
        ]
        for char in ESCAPE_CHARS:
            text = text.replace(char, f"\{char}")

        bot = Bot(self.media_session.access_token)
        logging.info([chat_id, text, photo])
        reply_markup = await generate_buttons_markup(buttons_info)
        if photo:
            msg = await bot.send_photo(chat_id=chat_id, caption=text, photo=FSInputFile(photo),
                                       reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
        else:
            msg = await bot.send_message(
                chat_id=chat_id,
                text=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2
            )
        logging.info(msg)
        return True  # TODO: make sure message is sent
