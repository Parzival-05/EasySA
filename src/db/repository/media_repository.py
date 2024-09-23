from src.db.models.media_model import MediaSessionModel, MediaPlatformModel
from src.db.models.streamer_model import StreamerModel
from src.db.repository.base_repository import Repository


class MediaPlatformRepository(Repository):
    MODEL = MediaPlatformModel


class MediaSessionRepository(Repository):
    MODEL = MediaSessionModel

    def get_media_session_by_name(self, name: str) -> MODEL:
        return self.get_one(name=name)

    def get_streamers_media_sessions(self, streamer: StreamerModel):
        return (
            self.db_session.query(self.MODEL)
            .filter_by(self.MODEL.streamers.contains(streamer))
            .all()
        )

    async def set_as_active(self, media_session: MediaSessionModel) -> bool:
        media_session.is_active = True
        await self.add(media_session)
        return True

    async def set_as_inactive(self, media_session: MediaSessionModel) -> bool:
        posts = media_session.posts
        for post in posts:
            if post.is_active:
                post.is_active = False
                await self.add(post)
        await self.add(media_session)
        return True

    async def delete(self, **filters) -> int:
        return self.db_session.query(self.MODEL).filter_by(**filters).delete()