from typing import Optional

from aiogram import F
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session

from src.bot.handlers.media import generate_media_info
from src.bot.handlers.streamer.post.post_router import post_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.post.media.generate_post_media_buttons import (
    get_post_media_sessions_inline_keyboard,
    get_post_media_session_actions_inline_keyboard,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.post.media.media_back_button import (
    get_post_medias_back_button,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.post.post_back_button import (
    get_post_back_button,
)
from src.bot.keyboards.buttons.post.post_buttons import PostActionButtons
from src.bot.keyboards.callback_data.streamer.post.post_cd import (
    EditPostCD,
)
from src.bot.keyboards.callback_data.streamer.post.post_media_cd import (
    GetPostMediaSessionCD,
)
from src.db.models.post_model import PostModel
from src.db.repository.association.post_media_repository import (
    PostMediaSessionJoinRepository,
)
from src.db.repository.media_repository import MediaSessionRepository
from src.db.repository.post_repository import PostRepository


@post_router.callback_query(
    EditPostCD.filter(F.post_action_button == PostActionButtons.EDIT_MEDIA)
)
async def return_post_medias(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: EditPostCD,
):
    post_repository = PostRepository(db_session)
    post = await post_repository.get_one(id=callback_data.post_id)
    post_media_session_join_repository = PostMediaSessionJoinRepository(db_session)
    media_session_repository = MediaSessionRepository(db_session)
    media_sessions_associated_with_streamer = (
        await media_session_repository.list_where_attr_contains_obj(
            streamers=post.streamer
        )
    )
    post_media_session_joins = list(
        filter(
            lambda x: x is not None,
            [
                await post_media_session_join_repository.get_one(
                    post_id=post.id, media_session_id=media_session.id
                )
                for media_session in media_sessions_associated_with_streamer
            ],
        )
    )
    go_back_button = get_post_back_button(post)
    reply_markup = await get_reply_markup(
        await get_post_media_sessions_inline_keyboard(
            post, post_media_session_joins, media_sessions_associated_with_streamer
        ),
        go_back_button,
    )
    await callback_query.message.edit_text(
        text="Доступные медиа",
        reply_markup=reply_markup,
    )


@post_router.callback_query(GetPostMediaSessionCD.filter())
async def return_post_media(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: GetPostMediaSessionCD,
):
    post_id = callback_data.post_id
    media_id = callback_data.media_id
    post_repository = PostRepository(db_session)
    media_session_repository = MediaSessionRepository(db_session)
    post: Optional[PostModel] = await post_repository.get_one(id=post_id)
    media_session = await media_session_repository.get_one(id=media_id)
    if not media_session:
        await callback_query.message.edit_text(
            text=f"Медиа не существует.",
        )
        return
    post_media_session_join_repository = PostMediaSessionJoinRepository(db_session)
    post_media_session_join = await post_media_session_join_repository.get_one(
        post_id=post_id, media_session_id=media_id
    )
    go_back_button = get_post_medias_back_button(post, PostActionButtons.EDIT_MEDIA)
    reply_markup = await get_reply_markup(
        await get_post_media_session_actions_inline_keyboard(
            post, media_session, post_media_session_join
        ),
        go_back_button,
    )
    await callback_query.message.edit_text(
        text=f"• Пост: {post.name}\n"
        f"• Постинг активен: {'Да' if post.is_active else 'Нет'}\n"
        f"------------------\n"
        f"{generate_media_info(media_session)}\n",
        reply_markup=reply_markup,
    )
