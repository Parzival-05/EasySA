from typing import Optional

from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from sqlalchemy.orm import Session

from src.bot.handlers.streamer.post.post_router import post_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.post.generate_post_buttons import (
    get_posts_inline_keyboard,
    get_post_actions_inline_keyboard,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.post.post_back_button import (
    get_posts_back_button,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.streamer_back_button import (
    get_streamer_back_button,
)
from src.bot.keyboards.buttons.streamer_buttons import StreamerInfoButtons
from src.bot.keyboards.callback_data.streamer.post.post_cd import AddPostCD, GetPostCD
from src.bot.keyboards.callback_data.streamer.streamer_cd import GetStreamerCD
from src.db.models.post_model import PostModel
from src.db.repository.post_repository import PostRepository
from src.db.repository.streamer_repository import StreamerRepository


@post_router.callback_query(
    GetStreamerCD.filter(F.streamer_info_button == StreamerInfoButtons.POSTS)
)
async def return_posts(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: GetStreamerCD,
):
    streamer_repository = StreamerRepository(db_session)
    streamer = await streamer_repository.get_one(id=callback_data.streamer_id)
    post_repository = PostRepository(db_session)
    add_new_post_button = InlineKeyboardButton(
        text="Добавить пост",
        callback_data=AddPostCD.from_id(streamer_id=callback_data.streamer_id).pack(),
    )
    go_back_button = get_streamer_back_button(streamer)
    reply_markup = await get_reply_markup(
        await get_posts_inline_keyboard(
            await post_repository.list(streamer_id=callback_data.streamer_id),
        ),
        add_new_post_button,
        go_back_button,
    )
    await callback_query.message.edit_text(
        text="Выберите пост", reply_markup=reply_markup
    )


@post_router.callback_query(GetPostCD.filter())
async def return_post(
    callback_query: CallbackQuery, db_session: Session, callback_data: GetPostCD
):
    post_id = callback_data.post_id
    post_repository = PostRepository(db_session)
    post: Optional[PostModel] = await post_repository.get_one(id=post_id)
    if not post:
        await callback_query.message.edit_text(
            text=f"Поста не существует.",
        )
        return
    go_back_button = get_posts_back_button(post.streamer)
    reply_markup = await get_reply_markup(
        await get_post_actions_inline_keyboard(post), go_back_button
    )
    await callback_query.message.edit_text(
        text=f"• Название: {post.name}\n"
        f"• Постинг активен: {'Да' if post.is_active else 'Нет'}\n"
        f"----------------------------\n"
        f"{post.text}\n"
        f"----------------------------",
        reply_markup=reply_markup,
    )
