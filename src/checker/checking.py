import asyncio
import logging
import traceback
from typing import Optional

from sqlalchemy.orm import Session

from config import AppConfig
from src.connection.messages import (
    PostStreamInfoMessage,
    ErrorMessage,
    DataMessage,
)
from src.domain.stream_platforms.sessions.base_platform_session import (
    BaseStreamPlatformSession,
)
from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)
from src.db.models.streamer_model import StreamerModel
from src.db.repository.streamer_repository import StreamerRepository


class Checker:
    def __init__(
        self,
        db_session: Session,
        stream_platform_sessions: list[BaseStreamPlatformSession],
    ):
        self.streamer_repository = StreamerRepository(db_session=db_session)
        self.stream_platform_sessions = stream_platform_sessions

    async def get_platform_session_by_platform_name(
        self, stream_platform_name: StreamPlatformNames
    ) -> Optional[BaseStreamPlatformSession]:
        for session in self.stream_platform_sessions:
            if session.PLATFORM_NAME == stream_platform_name:
                return session

    async def check_streamer(self, streamer: StreamerModel) -> Optional[DataMessage]:
        if not streamer.is_active:
            return
        stream_platform_session = await self.get_platform_session_by_platform_name(
            streamer.stream_platform_name
        )
        if stream_platform_session is None:
            return ErrorMessage(
                text=f"There is no session related to the {streamer = }. Probably you have entered the wrong "
                f"credentials for {streamer.stream_platform_name.value}."
            )
        try:
            stream_info = await stream_platform_session.get_stream_info(
                streamer.profile_id
            )
        except Exception as e:
            logging.exception(e)
            return ErrorMessage(
                text=f"Some unexpected error has occurred. Debug info:\n\n"
                + "\n".join(
                    traceback.format_exception(e.__class__, value=e, tb=e.__traceback__)
                )
            )
        logging.debug(f"{stream_info = }")
        if stream_info:
            return PostStreamInfoMessage(
                streamer_id=streamer.id, stream_info=stream_info
            )
        else:
            return None

    async def check_streamers(self) -> list[DataMessage]:
        streamers = await self.streamer_repository.get_active_streamers()
        data_messages = []
        for streamer in streamers:
            data_message = await self.check_streamer(streamer)
            if data_message:
                data_messages.append(data_message)
            await self.request_timeout()
        return data_messages

    @staticmethod
    async def request_timeout():
        await asyncio.sleep(AppConfig.REQUESTS_TIMEOUT)
