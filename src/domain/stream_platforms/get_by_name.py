from typing import Type

from src.domain.stream_platforms.platforms.twitch_platform import TwitchPlatform
from src.domain.stream_platforms.profiles.base_stream_profile import (
    BaseStreamProfile,
)
from src.domain.stream_platforms.sessions.base_platform_session import (
    BaseStreamPlatformSession,
)
from src.domain.stream_platforms.platforms.base_stream_platform import (
    BaseStreamPlatform,
)
from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)


def get_stream_platform_class(
    platform_name: StreamPlatformNames,
) -> Type[BaseStreamPlatform]:
    match platform_name:
        case StreamPlatformNames.Twitch:
            stream_platform_class = TwitchPlatform
        case _:
            raise RuntimeError("Unknown stream platform class")
    return stream_platform_class


def get_stream_platform_profile_class(
    platform_name: StreamPlatformNames,
) -> Type[BaseStreamProfile]:
    # noinspection PyTypeChecker
    return get_stream_platform_class(platform_name).PROFILE


def get_stream_platform_session_class(
    platform_name: StreamPlatformNames,
) -> Type[BaseStreamPlatformSession]:
    # noinspection PyTypeChecker
    return get_stream_platform_class(platform_name).SESSION
