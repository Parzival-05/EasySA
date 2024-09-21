from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.orm import Session

from src.bot.handlers.streamer.streamer_router import streamer_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.streamer_back_button import (
    get_streamer_back_button,
)
from src.bot.keyboards.buttons.streamer_buttons import StreamerActionButtons
from src.bot.keyboards.callback_data.streamer.streamer_cd import (
    EditStreamerCD,
)
from src.bot.keyboards.states.streamer_states import EditStreamerState
from src.db.models.streamer_model import StreamerModel
from src.db.repository.streamer_repository import StreamerRepository


@streamer_router.message(EditStreamerState.EDIT_NAME)
async def edit_name(
    message: Message,
    db_session: Session,
    state: FSMContext,
):
    context_data = await state.get_data()
    streamer_id = context_data.get("id")
    streamer_repository = StreamerRepository(db_session)
    streamer = await streamer_repository.get_one(id=streamer_id)
    go_back_button = get_streamer_back_button(streamer)
    await streamer_repository.update({"id": streamer_id}, name=message.text)
    await streamer_repository.commit()
    await state.clear()
    await message.answer(
        text="Имя успешно изменено!",
        reply_markup=await get_reply_markup(None, go_back_button),
    )


@streamer_router.callback_query(
    EditStreamerCD.filter(F.streamer_action_button == StreamerActionButtons.EDIT_NAME)
)
async def edit_name_intent(
    callback_query: CallbackQuery,
    callback_data: EditStreamerCD,
    state: FSMContext,
    db_session: Session,
):
    await state.update_data(id=callback_data.streamer_id)
    await state.set_state(EditStreamerState.EDIT_NAME)
    streamer_id = callback_data.streamer_id
    streamer_repository = StreamerRepository(db_session)
    streamer = await streamer_repository.get_one(id=streamer_id)
    go_back_button = get_streamer_back_button(streamer)
    await callback_query.message.edit_text(
        text="Введите новое имя стримера",
        reply_markup=await get_reply_markup(None, go_back_button),
    )


@streamer_router.callback_query(
    EditStreamerCD.filter(
        F.streamer_action_button == StreamerActionButtons.SET_AS_INACTIVE
    )
)
async def set_as_inactive(
    callback_query: CallbackQuery, db_session: Session, callback_data: EditStreamerCD
):
    streamer_id = callback_data.streamer_id
    streamer_repository = StreamerRepository(db_session)
    streamer = await streamer_repository.get_one(id=streamer_id)
    is_inactive = await streamer_repository.set_as_inactive(streamer)
    go_back_button = get_streamer_back_button(streamer)
    if is_inactive:
        await streamer_repository.commit()
        text = (
            f"Посты с анонсом стримов от {streamer.name} больше не будут публиковаться."
        )
    else:
        text = f"Нельзя изменить статус стримера {streamer.name}."
    await callback_query.message.edit_text(
        text=text, reply_markup=await get_reply_markup(None, go_back_button)
    )


@streamer_router.callback_query(
    EditStreamerCD.filter(
        F.streamer_action_button == StreamerActionButtons.SET_AS_ACTIVE
    )
)
async def set_as_active(
    callback_query: CallbackQuery, db_session: Session, callback_data: EditStreamerCD
):
    streamer_id = callback_data.streamer_id
    streamer_repository = StreamerRepository(db_session)
    streamer: StreamerModel = await streamer_repository.get_one(id=streamer_id)
    go_back_button = get_streamer_back_button(streamer)
    if await streamer_repository.set_as_active(streamer):
        await streamer_repository.commit()
        text = f"Посты с анонсом стримов от {streamer.name} будут публиковаться."
    else:
        text = f"Этого стримера нельзя сделать активным. Убедитесь, что у него есть хотя бы один активный пост."
    await callback_query.message.edit_text(
        text, reply_markup=await get_reply_markup(None, go_back_button)
    )
