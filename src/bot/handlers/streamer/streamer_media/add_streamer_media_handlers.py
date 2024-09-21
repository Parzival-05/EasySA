from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session

from src.bot.handlers.streamer.streamer_router import streamer_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.media.generate_streamer_media_buttons import (
    get_available_for_streamer_media_sessions_inline_keyboard,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.streamer_back_button import (
    get_streamer_back_button,
)
from src.bot.keyboards.callback_data.streamer.media.streamer_media_cd import (
    AddStreamerMediaSessionIntentCD,
    AddStreamerMediaSessionCD,
)
from src.db.models.association.post_media import PostMediaSessionJoin
from src.db.models.association.streamer_media_session import StreamerMediaSessionJoin
from src.db.repository.association.post_media_repository import (
    PostMediaSessionJoinRepository,
)
from src.db.repository.association.streamer_media_repository import (
    StreamerMediaSessionJoinRepository,
)
from src.db.repository.media_repository import MediaSessionRepository
from src.db.repository.streamer_repository import StreamerRepository


@streamer_router.callback_query(AddStreamerMediaSessionIntentCD.filter())
async def add_media_to_streamer_intent(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: AddStreamerMediaSessionIntentCD,
    # back_inline_button: InlineKeyboardButton,
):
    streamer_id = callback_data.streamer_id
    streamer_repository = StreamerRepository(db_session)
    media_session_repository = MediaSessionRepository(db_session)
    streamer = await streamer_repository.get_one(id=streamer_id)
    media_sessions_not_associated_with_streamer = (
        await (
            media_session_repository.list_where_attr_not_contains_obj(
                streamers=streamer
            )
        )
    )
    streamer_media_session_join_repository = StreamerMediaSessionJoinRepository(
        db_session
    )
    streamer_media_sessions_join_of_streamer = (
        await streamer_media_session_join_repository.list(streamer_id=streamer_id)
    )
    reply_markup = await get_reply_markup(
        await get_available_for_streamer_media_sessions_inline_keyboard(
            streamer,
            streamer_media_sessions_join_of_streamer,
            media_sessions_not_associated_with_streamer,
        ),
        # back_inline_button,
    )
    await callback_query.message.edit_text(
        text=f"Выберите медиа для стримера {streamer.name}",
        reply_markup=reply_markup,
    )


@streamer_router.callback_query(AddStreamerMediaSessionCD.filter())
async def add_media_to_streamer(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: AddStreamerMediaSessionCD,
):
    streamer_id = callback_data.streamer_id
    streamer_repository = StreamerRepository(db_session)
    streamer = await streamer_repository.get_one(id=streamer_id)
    media_session_repository = MediaSessionRepository(db_session)
    media_session = await media_session_repository.get_one(
        id=callback_data.media_session_id
    )
    post_media_session_join_repository = PostMediaSessionJoinRepository(db_session)
    for post in streamer.posts:
        post_media_session_join = PostMediaSessionJoin(
            post_id=post.id, media_session_id=media_session.id
        )
        await post_media_session_join_repository.add(post_media_session_join)
    streamer_media_session_join_repository = StreamerMediaSessionJoinRepository(
        db_session
    )
    streamer_media_session_join = StreamerMediaSessionJoin(
        streamer_id=streamer.id, media_session_id=media_session.id
    )
    await streamer_media_session_join_repository.add(streamer_media_session_join)
    await streamer_media_session_join_repository.commit()
    go_back_button = get_streamer_back_button(streamer)
    await callback_query.message.edit_text(
        text=f"Медиа {media_session.name} добавлено к стримеру",
        reply_markup=await get_reply_markup(None, go_back_button),
    )
