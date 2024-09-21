from src.bot.keyboards.callback_data.base_cd import BaseCD
from src.domain.media_platforms.media_names import MediaPlatformNames
from src.db.models.media_model import MediaPlatformModel


class GetMediaPlatformCD(BaseCD, prefix="GetMediaPlatformCD"):
    name: MediaPlatformNames

    @staticmethod
    def from_model(media_platform: MediaPlatformModel):
        return GetMediaPlatformCD(name=media_platform.name)
