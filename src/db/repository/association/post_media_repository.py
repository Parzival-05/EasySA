from src.db.models.association.post_media import PostMediaSessionJoin
from src.db.models.media_model import MediaSessionModel
from src.db.repository.base_repository import Repository
from src.db.repository.media_repository import MediaSessionRepository
from src.db.repository.post_repository import PostRepository
from src.db.repository.streamer_repository import StreamerRepository


class PostMediaSessionJoinRepository(Repository):
    MODEL = PostMediaSessionJoin

    async def set_as_inactive(self, post_media_session: PostMediaSessionJoin) -> bool:
        post_media_session.is_active = False
        post_id = post_media_session.post_id
        media_session_id = post_media_session.media_session_id
        media_session_repository = MediaSessionRepository(self.db_session)
        media_session: MediaSessionModel = await media_session_repository.get_one(
            id=media_session_id
        )

        post_repository = PostRepository(self.db_session)
        post = await post_repository.get_one(id=post_id)
        streamer = post.streamer
        streamer_posts = streamer.posts
        for streamer_post in streamer_posts:
            if (
                streamer_post.is_active
                and media_session not in streamer_post.media_sessions
            ):
                break
        else:
            streamer.is_active = False
            streamer_repository = StreamerRepository(self.db_session)
            await streamer_repository.add(streamer)
        return True

    async def set_as_active(self, post_media_session: PostMediaSessionJoin) -> bool:
        post_media_session.is_active = True
        await self.add(post_media_session)
        return True
