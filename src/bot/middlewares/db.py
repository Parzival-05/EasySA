from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, db_session):
        self.db_session = db_session

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        data["db_session"] = self.db_session
        return await handler(event, data)
