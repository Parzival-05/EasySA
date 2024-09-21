from typing import Type

from src.actor.base_media_actor import BaseMediaActor
from src.actor.discord_actor import DiscordActor
from src.actor.telegram_actor import TelegramActor
from src.domain.media_platforms.media_names import MediaPlatformNames


def get_media_actor_class(
    media_platform_name: MediaPlatformNames,
) -> Type[BaseMediaActor]:
    match media_platform_name:
        case MediaPlatformNames.TELEGRAM:
            media_actor_class = TelegramActor
        case MediaPlatformNames.DISCORD:
            media_actor_class = DiscordActor
        case _:
            raise RuntimeError("Unknown media actor class")
    return media_actor_class
