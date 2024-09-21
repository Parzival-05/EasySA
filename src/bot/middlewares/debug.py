import logging
from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import TelegramObject, Update

from src.bot.keyboards.utils import check_is_button_pressed


class DeleteMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        if isinstance(event, Update):
            if event.message:
                logging.debug(f"user_info: {event.message.from_user}")
                logging.debug(f"message = {event.message.text}")
                if await check_is_button_pressed(event.message.text):
                    try:
                        await event.message.delete()
                    except TelegramBadRequest:
                        pass
            elif event.callback_query:
                logging.debug(f"user_info: {event.callback_query.from_user}")
                logging.debug(f"callback_data = {event.callback_query.data}")
        return await handler(event, data)
