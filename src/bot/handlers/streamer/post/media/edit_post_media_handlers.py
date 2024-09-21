from aiogram import F
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session

from src.bot.handlers.streamer.post.post_router import post_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.post.media.media_back_button import (
    get_post_media_back_button,
)
from src.bot.keyboards.buttons.post.media.post_media_buttons import (
    PostMediaActionButtons,
)
from src.bot.keyboards.callback_data.streamer.post.post_media_cd import (
    EditPostMediaSessionCD,
)
from src.db.repository.association.post_media_repository import (
    PostMediaSessionJoinRepository,
)
from src.db.repository.media_repository import MediaSessionRepository
from src.db.repository.post_repository import PostRepository


@post_router.callback_query(
    EditPostMediaSessionCD.filter(
        F.post_media_action_button == PostMediaActionButtons.SET_AS_ACTIVE
    )
)
async def set_as_active(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: EditPostMediaSessionCD,
):
    post_id = callback_data.post_id
    media_session_id = callback_data.media_id
    post_media_session_join_repository = PostMediaSessionJoinRepository(db_session)
    post_media_session_join = await post_media_session_join_repository.get_one(
        post_id=post_id, media_session_id=media_session_id
    )
    post_repository = PostRepository(db_session)
    post = await post_repository.get_one(id=callback_data.post_id)
    media_session_repository = MediaSessionRepository(db_session)
    media_session = await media_session_repository.get_one(id=media_session_id)
    go_back_button = get_post_media_back_button(post, media_session)
    if await post_media_session_join_repository.set_as_active(post_media_session_join):
        await post_media_session_join_repository.commit()
        text = "Теперь медиа активно для поста."
    else:
        text = "Этот пост нельзя сделать активным для данного медиа."
    await callback_query.message.edit_text(
        text=text,
        reply_markup=await get_reply_markup(None, go_back_button),
    )


@post_router.callback_query(
    EditPostMediaSessionCD.filter(
        F.post_media_action_button == PostMediaActionButtons.SET_AS_INACTIVE
    )
)
async def set_as_inactive(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: EditPostMediaSessionCD,
):
    post_id = callback_data.post_id
    media_session_id = callback_data.media_id
    post_media_session_join_repository = PostMediaSessionJoinRepository(db_session)
    post_media_session_join = await post_media_session_join_repository.get_one(
        post_id=post_id, media_session_id=media_session_id
    )
    post_repository = PostRepository(db_session)
    post = await post_repository.get_one(id=callback_data.post_id)
    media_session_repository = MediaSessionRepository(db_session)
    media_session = await media_session_repository.get_one(id=media_session_id)
    go_back_button = get_post_media_back_button(post, media_session)
    if await post_media_session_join_repository.set_as_inactive(
        post_media_session_join
    ):
        await post_media_session_join_repository.commit()
        text = "Теперь медиа неактивно для поста."
    else:
        text = "Это медиа нельзя сделать неактивным для данного поста."
    await callback_query.message.edit_text(
        text=text, reply_markup=await get_reply_markup(None, go_back_button)
    )
