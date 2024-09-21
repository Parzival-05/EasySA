from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from sqlalchemy.orm import Session

from src.bot.handlers.streamer import streamer_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.media.generate_streamer_media_buttons import (
    get_streamer_media_sessions_inline_keyboard,
)
from src.bot.keyboards.buttons.menu_buttons import MediaButtons
from src.bot.keyboards.buttons.streamer_buttons import StreamerInfoButtons
from src.bot.keyboards.callback_data.streamer.media.streamer_media_cd import (
    GetStreamerMediaSessionCD,
    AddStreamerMediaSessionIntentCD,
)
from src.bot.keyboards.callback_data.streamer.streamer_cd import GetStreamerCD
from src.db.repository.association.streamer_media_repository import (
    StreamerMediaSessionJoinRepository,
)
from src.db.repository.streamer_repository import StreamerRepository


async def get_streamer_medias_reply(
    callback_query: CallbackQuery,
    db_session: Session,
    streamer_id: int,
):
    streamer_repository = StreamerRepository(db_session)
    streamer = await streamer_repository.get_one(id=streamer_id)
    add_media_inline_button = InlineKeyboardButton(
        text=MediaButtons.ADD,
        callback_data=AddStreamerMediaSessionIntentCD.from_model(streamer).pack(),
    )
    streamer_media_session_join_repository = StreamerMediaSessionJoinRepository(
        db_session
    )
    reply_markup = await get_reply_markup(
        await get_streamer_media_sessions_inline_keyboard(
            streamer,
            await streamer_media_session_join_repository.list(streamer_id=streamer_id),
        ),
        add_media_inline_button,
        InlineKeyboardButton(
            text="Назад",
            callback_data=GetStreamerCD.from_model(
                streamer, StreamerInfoButtons.STREAMER
            ).pack(),
        ),
    )
    await callback_query.message.edit_text(
        text="Выберите медиа", reply_markup=reply_markup
    )


@streamer_router.callback_query(
    GetStreamerCD.filter(F.streamer_info_button == StreamerInfoButtons.MEDIAS)
)
async def return_streamer_medias(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: GetStreamerCD,
):
    streamer_id = callback_data.streamer_id
    await get_streamer_medias_reply(
        callback_query,
        db_session,
        streamer_id,
    )


@streamer_router.callback_query(GetStreamerMediaSessionCD.filter())
async def return_streamer_media(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: GetStreamerMediaSessionCD,
):
    streamer_id = callback_data.streamer_id
    media_session_id = callback_data.media_session_id
    streamer_media_session_join_repository = StreamerMediaSessionJoinRepository(
        db_session
    )
    streamer_media_session_join = await streamer_media_session_join_repository.get_one(
        streamer_id=streamer_id, media_session_id=media_session_id
    )
    if streamer_media_session_join.is_active:
        await streamer_media_session_join_repository.set_as_inactive(
            streamer_media_session_join
        )
    else:
        await streamer_media_session_join_repository.set_as_active(
            streamer_media_session_join
        )
    await streamer_media_session_join_repository.add(streamer_media_session_join)
    await streamer_media_session_join_repository.commit()
    await get_streamer_medias_reply(callback_query, db_session, streamer_id)
