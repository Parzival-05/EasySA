from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

from src.db.models.media_model import MediaSessionModel, MediaPlatformModel


class BaseMediaProfileInfo(BaseModel, ABC):
    @abstractmethod
    def create_model(
        self, name: str, media_platform: MediaPlatformModel, is_active: bool = True
    ) -> MediaSessionModel: ...


class BaseMediaProfileInfoParser(ABC):
    @property
    @abstractmethod
    def PROFILE_INFO(self) -> Type[BaseMediaProfileInfo]: ...

    def __init__(self, text: str):
        self.text = text

    @abstractmethod
    async def parse(self) -> PROFILE_INFO: ...


class BaseMediaProfileValidator(ABC):
    @property
    @abstractmethod
    def PROFILE_INFO(self) -> Type[BaseMediaProfileInfo]: ...

    def __init__(self, profile_info: PROFILE_INFO):
        self.profile_info = profile_info

    @abstractmethod
    async def validate(self): ...


class BaseMediaProfile(ABC):

    @property
    @abstractmethod
    def PROFILE_INFO(self) -> Type[BaseMediaProfileInfo]: ...

    @property
    @abstractmethod
    def PROFILE_INFO_PARSER(self) -> Type[BaseMediaProfileInfoParser]: ...
    @property
    @abstractmethod
    def VALIDATOR(self) -> Type[BaseMediaProfileValidator]: ...

    async def get_profile_info(self, text):
        profile_info_parser = self.PROFILE_INFO_PARSER(text)
        profile_info = await profile_info_parser.parse()
        await self.VALIDATOR(profile_info).validate()
        return profile_info

    @staticmethod
    @abstractmethod
    def help() -> str: ...

    @staticmethod
    @abstractmethod
    def get_important_for_user_info(media_session: MediaSessionModel) -> str: ...
