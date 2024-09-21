from aiogram import F
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session

from src.bot.handlers.streamer.streamer_router import streamer_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.menu_back_button import (
    get_menu_back_button,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.generate_streamer_buttons import (
    get_streamers_inline_keyboard,
    get_streamer_actions_inline_keyboard,
)
from src.bot.keyboards.buttons.menu_buttons import StreamerButtons
from src.bot.keyboards.buttons.streamer_buttons import StreamerInfoButtons
from src.bot.keyboards.callback_data.menu_cd import MenuCD
from src.bot.keyboards.callback_data.streamer.streamer_cd import GetStreamerCD
from src.domain.stream_platforms.get_by_name import (
    get_stream_platform_profile_class,
)
from src.domain.stream_platforms.profiles.base_stream_profile import (
    StreamProfileInfo,
)
from src.db.repository.streamer_repository import StreamerRepository


@streamer_router.callback_query(MenuCD.filter(F.text == StreamerButtons.GET_LIST))
async def return_streamers(
    callback_query: CallbackQuery,
    db_session: Session,
):
    streamer_repository = StreamerRepository(db_session)
    reply_markup = await get_reply_markup(
        await get_streamers_inline_keyboard(await streamer_repository.list())
    )
    await callback_query.message.edit_text(
        text="Выберите стримера", reply_markup=reply_markup
    )


@streamer_router.callback_query(
    GetStreamerCD.filter(F.streamer_info_button == StreamerInfoButtons.STREAMER),
)
async def return_streamer(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: GetStreamerCD,
):
    streamer_id = callback_data.streamer_id
    streamer_repository = StreamerRepository(db_session)
    streamer = await streamer_repository.get_one(id=streamer_id)
    go_back_button = get_menu_back_button(StreamerButtons.GET_LIST)
    reply_markup = await get_reply_markup(
        await get_streamer_actions_inline_keyboard(streamer), go_back_button
    )
    stream_platform_profile_class = get_stream_platform_profile_class(
        streamer.stream_platform_name
    )
    streamer_profile_url = stream_platform_profile_class.generate_profile_url(
        StreamProfileInfo(profile_id=streamer.profile_id)
    )
    await callback_query.message.edit_text(
        text=f"• Имя: {streamer.name}\n"
        f"• Платформа: {streamer.stream_platform_name.value}\n"
        f"• Постинг активен: {'Да' if streamer.is_active else 'Нет'}\n"
        f"• Ссылка на профиль: {streamer_profile_url}",
        reply_markup=reply_markup,
    )
