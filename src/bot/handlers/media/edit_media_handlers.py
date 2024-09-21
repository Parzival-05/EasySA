from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.orm import Session

from src.bot.handlers.media import media_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.media.media_back_button import (
    get_media_session_back_button,
)
from src.bot.keyboards.buttons.media.media_session_buttons import (
    MediaSessionActionButtons,
)
from src.bot.keyboards.callback_data.media.media_session_cd import (
    EditMediaSessionCD,
)
from src.bot.keyboards.states.media.media_session_states import EditMediaSessionState
from src.db.repository.media_repository import MediaSessionRepository


@media_router.message(EditMediaSessionState.EDIT_NAME)
async def edit_name(
    message: Message,
    db_session: Session,
    state: FSMContext,
):
    context_data = await state.get_data()
    media_id = context_data.get("id")
    media_session_repository = MediaSessionRepository(db_session)
    media_session = await media_session_repository.get_one(id=media_id)
    go_back_button = get_media_session_back_button(media_session)
    await media_session_repository.update({"id": media_id}, name=message.text)
    await media_session_repository.commit()
    await state.clear()
    await message.answer(
        text="Имя успешно изменено!",
        reply_markup=await get_reply_markup(
            None,
            go_back_button,
        ),
    )


@media_router.callback_query(
    EditMediaSessionCD.filter(
        F.media_session_action_button == MediaSessionActionButtons.EDIT_NAME
    )
)
async def edit_name_intent(
    callback_query: CallbackQuery,
    callback_data: EditMediaSessionCD,
    db_session: Session,
    state: FSMContext,
):
    media_session_id = callback_data.media_session_id
    media_session_repository = MediaSessionRepository(db_session)
    media_session = await media_session_repository.get_one(id=media_session_id)
    go_back_button = get_media_session_back_button(media_session)
    await state.update_data(id=callback_data.media_session_id)
    await state.set_state(EditMediaSessionState.EDIT_NAME)
    await callback_query.message.edit_text(
        text="Введите новое имя медиа",
        reply_markup=await get_reply_markup(
            None,
            go_back_button,
        ),
    )
