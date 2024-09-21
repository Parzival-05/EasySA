from src.domain.stream_platforms.platforms.base_stream_platform import (
    BaseStreamPlatform,
)
from src.domain.stream_platforms.profiles.twitch_profile import (
    TwitchStreamProfile,
)
from src.domain.stream_platforms.sessions.twitch_session import TwitchSession
from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)


class TwitchPlatform(BaseStreamPlatform):
    PLATFORM_NAME = StreamPlatformNames.Twitch
    PROFILE = TwitchStreamProfile
    SESSION = TwitchSession
