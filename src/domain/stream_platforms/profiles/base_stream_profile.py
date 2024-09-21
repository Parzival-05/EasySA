from abc import abstractmethod, ABC
from typing import Type

from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.domain.stream_platforms.sessions.base_platform_session import (
    BaseStreamPlatformSession,
)
from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)


class StreamProfileInfo(BaseModel):
    profile_id: str


class BaseStreamProfileInfoParser(ABC):
    def __init__(self, text: str):
        self.text = text

    @abstractmethod
    async def parse(self) -> StreamProfileInfo: ...


class BaseStreamProfileValidator(ABC):
    @property
    @abstractmethod
    def PLATFORM_SESSION(self) -> Type[BaseStreamPlatformSession]: ...

    def __init__(
        self, profile_info: StreamProfileInfo, stream_platform_session: PLATFORM_SESSION
    ):
        self.profile_info = profile_info
        self.stream_platform_session = stream_platform_session

    @abstractmethod
    async def validate(self): ...


class BaseStreamProfile(ABC):
    @property
    @abstractmethod
    def PLATFORM_NAME(self) -> StreamPlatformNames: ...
    @property
    @abstractmethod
    def PROFILE_INFO_PARSER(self) -> Type[BaseStreamProfileInfoParser]: ...
    @property
    @abstractmethod
    def PROFILE_VALIDATOR(self) -> Type[BaseStreamProfileValidator]: ...

    profile_info: StreamProfileInfo

    def __init__(self, text: str, db_session: Session):
        self.text = text
        self.db_session = db_session

    async def get_profile_info(self):
        from src.domain.stream_platforms.get_by_name import (
            get_stream_platform_session_class,
        )

        profile_info_parser = self.PROFILE_INFO_PARSER(self.text)
        profile_info = await profile_info_parser.parse()
        stream_platform_session_class = get_stream_platform_session_class(
            self.PLATFORM_NAME
        )
        stream_platform_session = stream_platform_session_class(self.db_session)
        validator = self.PROFILE_VALIDATOR(profile_info, stream_platform_session)
        await validator.validate()
        return profile_info

    @staticmethod
    @abstractmethod
    def help() -> str: ...
    @staticmethod
    @abstractmethod
    def generate_profile_url(streamer_profile_info: StreamProfileInfo): ...
