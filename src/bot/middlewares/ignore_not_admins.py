import json
from types import NoneType
from typing import Callable, Dict, Awaitable, Any

import environs
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from config import CommonConfig


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
        env = environs.Env()
        env.read_env(CommonConfig.ENV_PATH)
        is_admin = id in list(map(int, json.loads(env.str("ADMIN_IDS"))))
        if is_admin:
            return await handler(event, data)
        else:
            return
