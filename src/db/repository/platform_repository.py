from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)
from src.db.models.platform_model import StreamPlatformSessionModel, StreamPlatformModel
from src.db.repository.base_repository import Repository


class StreamPlatformRepository(Repository):
    MODEL = StreamPlatformModel

    def get_by_platform_name(self, stream_platform_name: StreamPlatformNames):
        return self.get_one(name=stream_platform_name)


class StreamPlatformSessionRepository(Repository):
    MODEL = StreamPlatformSessionModel

    def get_by_platform_name(self, stream_platform_name: StreamPlatformNames):
        return self.get_one(stream_platform_name=stream_platform_name)
