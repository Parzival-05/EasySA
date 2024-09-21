from sqlalchemy.orm import sessionmaker

from src.domain.media_platforms.media_names import MediaPlatformNames
from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)
from src.db.models.engine import engine
from src.db.models.media_model import MediaPlatformModel
from src.db.models.platform_model import StreamPlatformSessionModel, StreamPlatformModel
from src.db.repository.media_repository import MediaPlatformRepository
from src.db.repository.platform_repository import StreamPlatformRepository


async def init_platforms():
    db_session = sessionmaker(bind=engine)()  # Sniffs?...
    stream_platform_repository = StreamPlatformRepository(db_session)

    async def create_stream_platform(stream_platform_name: StreamPlatformNames):
        stream_platform = StreamPlatformModel(name=stream_platform_name)
        stream_platform_session = StreamPlatformSessionModel()
        stream_platform.session = stream_platform_session
        await stream_platform_repository.add_all(
            [stream_platform_session, stream_platform]
        )

    for stream_platform_name in StreamPlatformNames:
        await create_stream_platform(stream_platform_name)
    await stream_platform_repository.commit()


async def delete_platforms():
    db_session = sessionmaker(bind=engine)()
    platform_repository = StreamPlatformRepository(db_session)
    await platform_repository.delete()
    await platform_repository.commit()


async def init_medias():
    db_session = sessionmaker(bind=engine)()
    media_repository = MediaPlatformRepository(db_session)

    async def create_media(media_name: MediaPlatformNames):
        media = MediaPlatformModel(name=media_name)
        await media_repository.add(media)

    for media_name in MediaPlatformNames:
        await create_media(media_name)
    await media_repository.commit()


async def delete_medias():
    db_session = sessionmaker(bind=engine)()
    media_repository = MediaPlatformRepository(db_session)
    await media_repository.delete()
    await media_repository.commit()
