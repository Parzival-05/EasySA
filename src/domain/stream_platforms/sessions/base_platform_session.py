import logging
import time
from abc import abstractmethod, ABC
from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel

from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)
from src.db.models.platform_model import StreamPlatformSessionModel
from src.db.repository.platform_repository import (
    StreamPlatformSessionRepository,
)


class StreamInfo(BaseModel):
    stream_id: int
    preview: Optional[str]
    title: str
    category: str


class BaseStreamPlatformSession(ABC):
    @property
    @abstractmethod
    def PLATFORM_NAME(self) -> StreamPlatformNames: ...

    def __init__(self, db_session):
        self.db_session = db_session

    async def auth(self):
        platform_session = await self.get_platform_session()
        if (
            platform_session
            and platform_session.refresh_token is not None
            and platform_session.expires_in < datetime.now()
        ):
            if platform_session.expires_in < datetime.now():
                session_info = await self.refresh_session(
                    platform_session.refresh_token
                )
            else:
                return
        else:
            session_info = await self._get_session_info()
        await self.save_session_info(**session_info)

    async def save_session_info(self, **session_info):
        ATTRS = StreamPlatformSessionModel.__table__.columns.keys()
        ATTRS.remove("id")
        platform_session = await self.get_platform_session()
        platform_session_repository = StreamPlatformSessionRepository(self.db_session)
        if platform_session:
            await platform_session_repository.update_one(
                platform_session, **session_info
            )
        else:
            raise PlatformNotInDB
        await platform_session_repository.commit()

    async def get_platform_session(self) -> StreamPlatformSessionModel:
        platform_session_repository = StreamPlatformSessionRepository(self.db_session)
        platform_session = await platform_session_repository.get_by_platform_name(
            self.PLATFORM_NAME
        )
        return platform_session

    @staticmethod
    def check_if_expired(func):
        async def wrapper(self, *args, **kwargs):
            async def refresh_and_save():
                session_info = await self.refresh_session()
                await self.save_session_info(**session_info)

            platform_session = await self.get_platform_session()
            if datetime.fromtimestamp(time.time()) > platform_session.expires_in:
                await refresh_and_save()
            try:
                return await func(self, *args, **kwargs)
            except SessionExpired:
                await refresh_and_save()
                return await func(self, *args, **kwargs)

        return wrapper

    @abstractmethod
    async def _get_session_info(self) -> dict: ...

    @abstractmethod
    async def refresh_session(self, *args, **kwargs) -> Any: ...

    @abstractmethod
    async def get_stream_info(
        self, user_id: int, *args, **kwargs
    ) -> Optional[StreamInfo]: ...


class SessionExpired(Exception):
    def __init__(self, msg, error: Exception):
        logging.exception(msg, error)
        self.error = error
        super().__init__(SessionExpired, error)


class NonActiveSession(Exception):
    pass


class NonActiveStreamer(Exception):
    pass


class InvalidUser(Exception):
    pass


class PlatformNotInDB(Exception):
    pass
