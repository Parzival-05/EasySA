from typing import Type

from src.domain.media_platforms.media_names import MediaPlatformNames
from src.domain.media_platforms.profiles.base_media_profile import (
    BaseMediaProfile,
)
from src.domain.media_platforms.profiles.discord_profile import DiscordMediaProfile
from src.domain.media_platforms.profiles.telegram_profile import (
    TelegramMediaProfile,
)


def get_media_profile_class(
    media_platform_name: MediaPlatformNames,
) -> Type[BaseMediaProfile]:
    match media_platform_name:
        case MediaPlatformNames.TELEGRAM:
            media_platform_class = TelegramMediaProfile
        case MediaPlatformNames.DISCORD:
            media_platform_class = DiscordMediaProfile
        case _:
            raise RuntimeError("Unknown media profile class")
    return media_platform_class
