from aiogram import F
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session

from src.bot.handlers.streamer.post.post_router import post_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.post.generate_post_buttons import (
    get_post_deletion_inline_keyboard,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.post.post_back_button import (
    get_post_back_button,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.streamer_back_button import (
    get_streamer_back_button,
)
from src.bot.keyboards.buttons.post.post_buttons import PostActionButtons
from src.bot.keyboards.callback_data.streamer.post.post_cd import (
    DeletePostCD,
    EditPostCD,
)
from src.db.repository.post_repository import PostRepository


@post_router.callback_query(DeletePostCD.filter())
async def delete(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: DeletePostCD,
):
    post_id = callback_data.post_id
    post_repository = PostRepository(db_session)
    post = await post_repository.get_one(id=post_id)
    if not callback_data.confirm:
        text = "Удаление отменено."
        go_back_button = get_post_back_button(post)
    else:
        text = f"Пост {post.name} стримера {post.streamer.name} удален."
        go_back_button = get_streamer_back_button(post.streamer)
        await post_repository.delete(id=post_id)
        await post_repository.commit()
    reply_markup = await get_reply_markup(None, go_back_button)
    await callback_query.message.edit_text(
        text=text,
        reply_markup=reply_markup,
    )


@post_router.callback_query(
    EditPostCD.filter(F.post_action_button == PostActionButtons.DELETE)
)
async def delete_intent(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: EditPostCD,
):
    post_id = callback_data.post_id
    post_repository = PostRepository(db_session)
    post = await post_repository.get_one(id=post_id)
    go_back_button = get_post_back_button(post)
    reply_markup = await get_reply_markup(
        await get_post_deletion_inline_keyboard(post), go_back_button
    )
    await callback_query.message.edit_text(
        text="Вы уверены, что хотите удалить пост?",
        reply_markup=reply_markup,
    )
