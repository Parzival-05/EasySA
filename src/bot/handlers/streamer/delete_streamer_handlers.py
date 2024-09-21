from aiogram import F
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session

from src.bot.handlers.streamer.streamer_router import streamer_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.generate_streamer_buttons import (
    get_streamer_deletion_inline_keyboard,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.streamer_back_button import (
    get_streamer_back_button,
)
from src.bot.keyboards.buttons.streamer_buttons import (
    StreamerActionButtons,
)
from src.bot.keyboards.callback_data.streamer.streamer_cd import (
    DeleteStreamerCD,
    EditStreamerCD,
)
from src.db.repository.streamer_repository import StreamerRepository


@streamer_router.callback_query(DeleteStreamerCD.filter())
async def delete(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: DeleteStreamerCD,
):
    streamer_id = callback_data.streamer_id
    streamer_repository = StreamerRepository(db_session)
    streamer = await streamer_repository.get_one(id=streamer_id)
    go_back_button = get_streamer_back_button(streamer)
    if not callback_data.confirm:
        reply_markup = await get_reply_markup(
            await get_streamer_deletion_inline_keyboard(streamer), go_back_button
        )
        text = "Удаление отменено."
    else:
        await streamer_repository.delete(id=streamer_id)
        await streamer_repository.commit()
        reply_markup = None
        text = f"Стример {streamer.name} удален."
    await callback_query.message.edit_text(text=text, reply_markup=reply_markup)


@streamer_router.callback_query(
    EditStreamerCD.filter(F.streamer_action_button == StreamerActionButtons.DELETE)
)
async def delete_intent(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: EditStreamerCD,
):
    streamer_id = callback_data.streamer_id
    streamer_repository = StreamerRepository(db_session)
    streamer = await streamer_repository.get_one(id=streamer_id)
    go_back_button = get_streamer_back_button(streamer)
    reply_markup = await get_reply_markup(
        await get_streamer_deletion_inline_keyboard(streamer), go_back_button
    )
    await callback_query.message.edit_text(
        text=f"Вы уверены, что хотите безвозвратно удалить всю информацию о стримере {streamer.name}?",
        reply_markup=reply_markup,
    )
