import logging
from pathlib import Path
from typing import Optional

import telebot

from src.actor.base_media_actor import BaseMediaActor
from src.checker.post_info import PostVariables
from src.domain.stream_platforms.get_by_name import get_stream_platform_profile_class
from src.domain.stream_platforms.profiles.base_stream_profile import StreamProfileInfo


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

    def _send_post(
        self, chat_id: CHAT_ID_TYPE, text: str, photo: Optional[str] = None, **kwargs
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

        bot = telebot.TeleBot(self.media_session.access_token, parse_mode="MarkdownV2")
        logging.info([chat_id, text, photo])
        if photo:
            msg = bot.send_photo(chat_id=chat_id, caption=text, photo=open(photo, "rb"))
        else:
            msg = bot.send_message(
                chat_id=chat_id,
                text=text,
            )
        logging.info(msg)
        return True  # TODO: make sure message is sent
