from abc import ABC, abstractmethod
from typing import TypeVar, Optional

from src.db.models.media_model import MediaSessionModel
from src.db.models.post_model import PostModel
from src.db.models.streamer_model import StreamerModel
from src.domain.stream_platforms.sessions.base_platform_session import StreamInfo

T = TypeVar("T")


class BaseMediaActor(ABC):
    def __init__(
            self,
            post: PostModel,
            streamer: StreamerModel,
            media_session: MediaSessionModel,
            stream_info: StreamInfo,
    ):
        self.post = post
        self.streamer = streamer
        self.media_session = media_session
        self.stream_info = stream_info

    @property
    @abstractmethod
    def CHAT_ID_TYPE(self) -> T: ...

    @abstractmethod
    def get_chat_id(self) -> Optional[CHAT_ID_TYPE]: ...

    @abstractmethod
    def _get_text(self): ...

    @abstractmethod
    async def _send_post(
            self, chat_id: CHAT_ID_TYPE, text: str, photo: Optional[str] = None, **kwargs
    ): ...

    async def send_post(self):
        chat_id = self.get_chat_id()
        text = self._get_text()
        preview = self.post.preview.file_path if self.post.preview.file_path else self.stream_info.preview
        return await self._send_post(chat_id, text, preview)
