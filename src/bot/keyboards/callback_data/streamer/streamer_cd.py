from src.bot.keyboards.buttons.common import DeletionButtons
from src.bot.keyboards.buttons.streamer_buttons import (
    StreamerActionButtons,
    StreamerInfoButtons,
)
from src.bot.keyboards.callback_data.base_cd import BaseCD
from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)
from src.db.models.streamer_model import StreamerModel


class BaseStreamerCD(BaseCD, prefix="BaseStreamerCD"):
    streamer_id: int


class GetStreamerCD(BaseStreamerCD, prefix="GetStreamerCD"):
    streamer_info_button: StreamerInfoButtons

    @staticmethod
    def from_model(streamer: StreamerModel, streamer_info_button: StreamerInfoButtons):
        return GetStreamerCD(
            streamer_id=streamer.id, streamer_info_button=streamer_info_button
        )


class EditStreamerCD(BaseStreamerCD, prefix="EditStreamerCD"):
    streamer_action_button: StreamerActionButtons

    @staticmethod
    def from_model(
        streamer: StreamerModel, streamer_action_button: StreamerActionButtons
    ):
        return EditStreamerCD(
            streamer_id=streamer.id, streamer_action_button=streamer_action_button
        )


class DeleteStreamerCD(BaseStreamerCD, prefix="DeleteStreamerCD"):
    confirm: bool

    @staticmethod
    def from_model(streamer: StreamerModel, confirm: DeletionButtons):
        return DeleteStreamerCD(
            streamer_id=streamer.id, confirm=confirm == DeletionButtons.CONFIRM
        )


class GetPlatformNameCD(BaseCD, prefix="GetPlatformNameCD"):
    stream_platform_name: StreamPlatformNames

    @staticmethod
    def from_platform_name(stream_platform_name: StreamPlatformNames):
        return GetPlatformNameCD(stream_platform_name=stream_platform_name)
