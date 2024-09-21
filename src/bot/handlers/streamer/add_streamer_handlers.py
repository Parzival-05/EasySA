import logging

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.orm import Session

from src.bot.handlers.streamer.streamer_router import streamer_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.generate_streamer_buttons import (
    get_streamer_platforms_inline_keyboard,
)
from src.bot.keyboards.buttons.menu_buttons import StreamerButtons
from src.bot.keyboards.callback_data.menu_cd import MenuCD
from src.bot.keyboards.callback_data.streamer.streamer_cd import GetPlatformNameCD
from src.bot.keyboards.states.streamer_states import AddStreamerState
from src.domain.stream_platforms.get_by_name import (
    get_stream_platform_profile_class,
)
from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)
from src.db.models.streamer_model import StreamerModel
from src.db.repository.streamer_repository import StreamerRepository


@streamer_router.callback_query(MenuCD.filter(F.text == StreamerButtons.ADD))
async def add_streamer_start(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(AddStreamerState.GET_NAME)
    await callback_query.message.edit_text(text="Введите имя стримера")


@streamer_router.message(AddStreamerState.GET_NAME)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddStreamerState.CHOOSE_PLATFORM)
    reply_markup = await get_reply_markup(
        await get_streamer_platforms_inline_keyboard()
    )
    await message.answer(text="Выберите платформу стримера", reply_markup=reply_markup)


@streamer_router.callback_query(
    GetPlatformNameCD.filter(), AddStreamerState.CHOOSE_PLATFORM
)
async def choose_platform(
    callback_query: CallbackQuery, callback_data: GetPlatformNameCD, state: FSMContext
):
    stream_platform_name = callback_data.stream_platform_name
    stream_platform_profile_class = get_stream_platform_profile_class(
        stream_platform_name
    )
    await state.update_data(stream_platform_name=stream_platform_name)
    await state.set_state(AddStreamerState.GET_PROFILE)
    await callback_query.message.edit_text(text=stream_platform_profile_class.help())


@streamer_router.message(F.text, AddStreamerState.GET_PROFILE)
async def get_profile(message: Message, db_session: Session, state: FSMContext):
    profile = message.text
    context_data = await state.get_data()
    await state.clear()
    stream_platform_name: StreamPlatformNames = context_data.get("stream_platform_name")
    stream_platform_profile_class = get_stream_platform_profile_class(
        stream_platform_name
    )

    try:
        stream_platform_profile = stream_platform_profile_class(profile, db_session)
        profile_info = await stream_platform_profile.get_profile_info()
        streamer_repository = StreamerRepository(db_session)
        streamer = StreamerModel(
            name=context_data.get("name"),
            stream_platform_name=stream_platform_name,
            profile_id=profile_info.profile_id,
            media_sessions=[],
            posts=[],
            is_active=False,
        )
        await streamer_repository.add(streamer)
        await streamer_repository.commit()
        await message.answer(
            text=f"✅ Стример {streamer.name} добавлен. Теперь, перед его активацией, нужно добавить к нему пост с "
            f"текстом сообщения."
        )
    except Exception as e:
        logging.exception(e)
        await message.answer(text=f"❌ Стример не добавлен. {str(e)}")
