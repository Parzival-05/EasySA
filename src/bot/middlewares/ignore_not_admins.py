from types import NoneType
from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from config import TGBotConfig


class IgnoreNotAdminsMiddleware(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        if isinstance(event.message, NoneType):
            id = event.callback_query.from_user.id
        elif isinstance(event, Update):
            id = event.message.chat.id
        else:
            id = None
        is_admin = id in TGBotConfig.ADMIN_IDS
        if is_admin:
            return await handler(event, data)
        else:
            return
