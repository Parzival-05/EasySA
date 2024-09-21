from abc import abstractmethod, ABC
from typing import Type

from src.domain.stream_platforms.profiles.base_stream_profile import (
    BaseStreamProfile,
)
from src.domain.stream_platforms.sessions.base_platform_session import (
    BaseStreamPlatformSession,
)
from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)
from config import CommonConfig


class BaseStreamPlatform(ABC):
    @property
    @abstractmethod
    def PLATFORM_NAME(self) -> StreamPlatformNames: ...

    @property
    @abstractmethod
    def PROFILE(self) -> Type[BaseStreamProfile]: ...
    @property
    @abstractmethod
    def SESSION(self) -> Type[BaseStreamPlatformSession]: ...

    @staticmethod
    def get_nonactive_stream_preview_path():
        """Get default image preview in case of download failure"""
        return CommonConfig.STATIC_PATH + "twitch-404_preview-1920x1080.jpg"
