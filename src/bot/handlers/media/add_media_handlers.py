import logging

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.orm import Session

from src.bot.handlers.media.media_router import media_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.media.generate_media_session_buttons import (
    get_media_platforms_to_add_inline_keyboard,
)
from src.bot.keyboards.buttons.menu_buttons import MediaButtons
from src.bot.keyboards.callback_data.media.media_session_cd import AddMediaSessionCD
from src.bot.keyboards.callback_data.menu_cd import MenuCD
from src.bot.keyboards.states.post.media_states import AddMediaState
from src.db.repository.media_repository import (
    MediaPlatformRepository,
    MediaSessionRepository,
)
from src.domain.media_platforms.get_by_name import get_media_profile_class


@media_router.callback_query(MenuCD.filter(F.text == MediaButtons.ADD))
async def start_adding_of_media_session(
    callback_query: CallbackQuery, db_session: Session, state: FSMContext
):
    media_platform_repository = MediaPlatformRepository(db_session)
    reply_markup = await get_reply_markup(
        await get_media_platforms_to_add_inline_keyboard(
            await media_platform_repository.list()
        )
    )
    await state.set_state(AddMediaState.SELECT_PLATFORM)
    await callback_query.message.edit_text(
        text="Выберите медиаплатформу", reply_markup=reply_markup
    )


@media_router.callback_query(AddMediaSessionCD.filter(), AddMediaState.SELECT_PLATFORM)
async def select_platform(
    callback_query: CallbackQuery, state: FSMContext, callback_data: AddMediaSessionCD
):
    await state.update_data(media_platform_name=callback_data.media_platform_name)
    await state.set_state(AddMediaState.ADD_NAME)
    await callback_query.message.edit_text(
        text="Введите название медиа. Название должно быть уникальным."
    )


@media_router.message(AddMediaState.ADD_NAME)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    context_data = await state.get_data()
    media_platform_name = context_data.get("media_platform_name")
    media_profile_class = get_media_profile_class(media_platform_name)
    await state.set_state(AddMediaState.ADD_CREDS)
    await message.answer(text=media_profile_class.help())


@media_router.message(AddMediaState.ADD_CREDS)
async def add_creds(message: Message, db_session: Session, state: FSMContext):
    context_data = await state.get_data()
    media_platform_name = context_data.get("media_platform_name")
    media_profile = get_media_profile_class(media_platform_name)()
    try:
        profile_info = await media_profile.get_profile_info(message.text)
        media_platform_repository = MediaPlatformRepository(db_session)
        media_platform = await media_platform_repository.get_one(
            name=media_platform_name
        )
        media_session = profile_info.create_model(
            name=context_data.get("name"), media_platform=media_platform
        )
        media_session_repository = MediaSessionRepository(db_session)
        await media_session_repository.add(media_session)
        await media_session_repository.commit()
        await message.answer(text=f"Медиа {media_session.name} добавлено.")
    except Exception as e:
        logging.exception(e)
        await message.answer("Произошла ошибка")
    finally:
        await state.clear()
