from aiogram import F
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session

from src.bot.handlers.media import media_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.media.generate_media_session_buttons import (
    get_media_session_deletion_inline_keyboard,
)
from src.bot.keyboards.buttons.generate_buttons.media.media_back_button import (
    get_media_session_back_button,
)
from src.bot.keyboards.buttons.media.media_session_buttons import (
    MediaSessionActionButtons,
)
from src.bot.keyboards.callback_data.media.media_session_cd import (
    DeleteMediaSessionCD,
    EditMediaSessionCD,
)
from src.db.repository.association.post_media_repository import (
    PostMediaSessionJoinRepository,
)
from src.db.repository.association.streamer_media_repository import (
    StreamerMediaSessionJoinRepository,
)
from src.db.repository.media_repository import MediaSessionRepository


@media_router.callback_query(DeleteMediaSessionCD.filter())
async def delete(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: DeleteMediaSessionCD,
):
    media_session_id = callback_data.media_session_id
    media_session_repository = MediaSessionRepository(db_session)
    media_session = await media_session_repository.get_one(id=media_session_id)
    if not callback_data.confirm:
        text = "Удаление отменено."
        go_back_button = get_media_session_back_button(media_session)
        reply_markup = await get_reply_markup(
            None,
            go_back_button,
        )
    else:
        await media_session_repository.delete(id=media_session_id)
        streamer_media_session_join_repository = StreamerMediaSessionJoinRepository(
            db_session
        )
        await streamer_media_session_join_repository.delete(
            media_session_id=media_session_id
        )
        post_media_session_join_repository = PostMediaSessionJoinRepository(db_session)
        await post_media_session_join_repository.delete(
            media_session_id=media_session_id
        )
        await streamer_media_session_join_repository.commit()
        text = "Медиа удалено."
        reply_markup = None
    await callback_query.message.edit_text(text=text, reply_markup=reply_markup)


@media_router.callback_query(
    EditMediaSessionCD.filter(
        F.media_session_action_button == MediaSessionActionButtons.DELETE
    )
)
async def delete_intent(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: EditMediaSessionCD,
):
    media_session_id = callback_data.media_session_id
    media_session_repository = MediaSessionRepository(db_session)
    media_session = await media_session_repository.get_one(id=media_session_id)
    go_back_button = get_media_session_back_button(media_session)
    reply_markup = await get_reply_markup(
        await get_media_session_deletion_inline_keyboard(media_session), go_back_button
    )
    await callback_query.message.edit_text(
        text="Вы уверены, что хотите удалить медиа?",
        reply_markup=reply_markup,
    )
