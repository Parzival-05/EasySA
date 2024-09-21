import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from sqlalchemy.orm import Session

from src.bot.handlers.media import media_router
from src.bot.handlers.menu_handlers import menu_router
from src.bot.handlers.streamer.post import post_router
from src.bot.handlers.streamer.streamer_router import streamer_router
from src.bot.keyboards.main_menu import get_menu
from src.bot.middlewares.db import DBSessionMiddleware
from src.bot.middlewares.debug import DeleteMessageMiddleware
from src.bot.middlewares.ignore_not_admins import IgnoreNotAdminsMiddleware
from src.bot.settings import get_bot_token
from src.bot.utils.set_commands import set_commands
from src.db.models.engine import db_session


async def start_bot(bot: Bot):
    await set_commands(bot)


def register_routers(dp: Dispatcher):
    dp.include_router(menu_router)
    dp.include_router(streamer_router)
    dp.include_router(post_router)
    dp.include_router(media_router)


async def main(db_session: Session):
    BOT_TOKEN = get_bot_token()
    bot = Bot(
        BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(bot=bot)
    dp.update.middleware(IgnoreNotAdminsMiddleware())
    dp.update.middleware(DBSessionMiddleware(db_session))
    dp.update.middleware(DeleteMessageMiddleware())
    dp.startup.register(start_bot)
    dp.message.register(get_menu, Command(commands="start"))
    register_routers(dp)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main(db_session))
