from src.bot.keyboards.buttons.post.media.post_media_buttons import (
    PostMediaActionButtons,
)
from src.bot.keyboards.callback_data.streamer.post.post_cd import BasePostCD
from src.db.models.media_model import MediaSessionModel
from src.db.models.post_model import PostModel


class BasePostMediaSessionCD(BasePostCD, prefix="BasePostMediaSessionCD"):
    media_id: int


class GetPostMediaSessionCD(BasePostMediaSessionCD, prefix="GetPostMediaSessionCD"):
    @staticmethod
    def from_model(post: PostModel, media_session: MediaSessionModel):
        return GetPostMediaSessionCD(post_id=post.id, media_id=media_session.id)


class EditPostMediaSessionCD(BasePostMediaSessionCD, prefix="EditPostMediaSessionCD"):
    post_media_action_button: PostMediaActionButtons

    @staticmethod
    def from_model(
        post: PostModel,
        media_session: MediaSessionModel,
        post_media_action_button: PostMediaActionButtons,
    ):
        return EditPostMediaSessionCD(
            post_id=post.id,
            media_id=media_session.id,
            post_media_action_button=post_media_action_button,
        )
