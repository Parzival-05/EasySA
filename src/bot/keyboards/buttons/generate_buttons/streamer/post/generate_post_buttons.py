from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards.buttons.common import DeletionButtons
from src.bot.keyboards.buttons.post.post_buttons import (
    PostActionButtons,
)
from src.bot.keyboards.buttons.post.preview_buttons import PostPreviewButtons
from src.bot.keyboards.callback_data.streamer.post.post_cd import (
    GetPostCD,
    EditPostCD,
    DeletePostCD,
)
from src.bot.keyboards.callback_data.streamer.post.preview_cd import (
    GetPostPreviewTypeCD,
)
from src.db.models.post_model import PostModel


# ********************************************** Get post **********************************************


async def get_posts_inline_keyboard(posts: list[PostModel]):
    def generate_text(post: PostModel) -> str:
        is_active = "🟢 Активен" if post.is_active else "🔴 Не активен"
        return f"{post.name} | {is_active}"

    keyboard_build = InlineKeyboardBuilder()
    for post in posts:
        keyboard_build.button(
            text=generate_text(post), callback_data=GetPostCD.from_model(post)
        )
    return keyboard_build.adjust(1)


# ********************************************** Edit post **********************************************


async def get_post_actions_inline_keyboard(post: PostModel):
    keyboard_build = InlineKeyboardBuilder()
    post_action_buttons: list[PostActionButtons] = [
        PostActionButtons.EDIT_MEDIA,
        PostActionButtons.EDIT_NAME,
        PostActionButtons.EDIT_TEXT,
        PostActionButtons.DELETE,
        (
            PostActionButtons.SET_AS_INACTIVE
            if post.is_active
            else PostActionButtons.SET_AS_ACTIVE
        ),
    ]
    for post_action_button in post_action_buttons:
        keyboard_build.button(
            text=post_action_button,
            callback_data=EditPostCD.from_model(post, post_action_button),
        )
    return keyboard_build.adjust(2)


# ********************************************** Delete post **********************************************
async def get_post_deletion_inline_keyboard(post: PostModel):
    keyboard_build = InlineKeyboardBuilder()
    deletion_buttons: list[DeletionButtons] = [
        DeletionButtons.CONFIRM,
    ]
    for button in deletion_buttons:
        keyboard_build.button(
            text=button,
            callback_data=DeletePostCD.from_model(post, button),
        )
    return keyboard_build


# ********************************************** Add post **********************************************
async def get_choose_media_type_inline_keyboard():
    keyboard_build = InlineKeyboardBuilder()
    for button in PostPreviewButtons:
        keyboard_build.button(
            text=button,
            callback_data=GetPostPreviewTypeCD.from_post_media_button(
                PostPreviewButtons(button)
            ),
        )
    return keyboard_build
