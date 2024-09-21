from src.bot.keyboards.buttons.common import DeletionButtons
from src.bot.keyboards.buttons.media.media_session_buttons import (
    MediaSessionActionButtons,
)
from src.bot.keyboards.callback_data.base_cd import BaseCD
from src.domain.media_platforms.media_names import MediaPlatformNames
from src.db.models.media_model import MediaSessionModel, MediaPlatformModel


class BaseMediaSessionCD(BaseCD, prefix="BaseMediaSessionCD"):
    media_session_id: int


class GetMediaSessionCD(BaseMediaSessionCD, prefix="GetMediaSessionCD"):
    media_session_id: int

    @staticmethod
    def from_model(media_session: MediaSessionModel):
        return GetMediaSessionCD(media_session_id=media_session.id)


class EditMediaSessionCD(BaseMediaSessionCD, prefix="EditMediaSessionCD"):
    media_session_action_button: MediaSessionActionButtons

    @staticmethod
    def from_model(
        media_session: MediaSessionModel,
        media_session_action_button: MediaSessionActionButtons,
    ):
        return EditMediaSessionCD(
            media_session_id=media_session.id,
            media_session_action_button=media_session_action_button,
        )


class DeleteMediaSessionCD(BaseMediaSessionCD, prefix="DeleteMediaSessionCD"):
    confirm: bool

    @staticmethod
    def from_model(media_session: MediaSessionModel, confirm: DeletionButtons):
        return DeleteMediaSessionCD(
            media_session_id=media_session.id,
            confirm=confirm == DeletionButtons.CONFIRM,
        )


class AddMediaSessionCD(BaseCD, prefix="AddMediaSessionCD"):
    media_platform_name: MediaPlatformNames

    @staticmethod
    def from_model(media_platform: MediaPlatformModel):
        return AddMediaSessionCD(media_platform_name=media_platform.name)
