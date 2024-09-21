from pydantic import BaseModel

from src.domain.stream_platforms.sessions.base_platform_session import (
    StreamInfo,
)


class DataMessage(BaseModel):
    pass


class TextMessage(DataMessage):
    text: str


class ErrorMessage(TextMessage):
    pass


class PostStreamInfoMessage(DataMessage):
    streamer_id: int
    stream_info: StreamInfo
