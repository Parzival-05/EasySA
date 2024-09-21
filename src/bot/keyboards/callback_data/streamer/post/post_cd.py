from src.bot.keyboards.buttons.common import DeletionButtons
from src.bot.keyboards.buttons.post.post_buttons import (
    PostActionButtons,
)
from src.bot.keyboards.callback_data.base_cd import BaseCD
from src.bot.keyboards.callback_data.streamer.streamer_cd import BaseStreamerCD
from src.db.models.post_model import PostModel


class BasePostCD(BaseCD, prefix="BasePostCD"):
    post_id: int


class GetPostCD(BasePostCD, prefix="GetPostCD"):
    @staticmethod
    def from_model(post: PostModel):
        return GetPostCD(post_id=post.id)


class EditPostCD(BasePostCD, prefix="EditPostCD"):
    post_action_button: PostActionButtons

    @staticmethod
    def from_model(post: PostModel, post_action_button: PostActionButtons):
        return EditPostCD(
            post_id=post.id,
            post_action_button=post_action_button,
        )


class DeletePostCD(BasePostCD, prefix="DeletePostCD"):
    confirm: bool

    @staticmethod
    def from_model(post: PostModel, confirm: DeletionButtons):
        return DeletePostCD(
            post_id=post.id,
            confirm=confirm == DeletionButtons.CONFIRM,
        )


class AddPostCD(BaseStreamerCD, prefix="AddPostCD"):
    @staticmethod
    def from_id(streamer_id: int):
        return AddPostCD(streamer_id=streamer_id)
