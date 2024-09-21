import logging

from src.db.models.association.streamer_media_session import StreamerMediaSessionJoin
from src.db.repository.association.post_media_repository import (
    PostMediaSessionJoinRepository,
)
from src.db.repository.base_repository import Repository
from src.db.repository.media_repository import MediaSessionRepository
from src.db.repository.streamer_repository import StreamerRepository


class StreamerMediaSessionJoinRepository(Repository):
    MODEL = StreamerMediaSessionJoin

    async def set_as_inactive(
        self, streamer_media_session_join: StreamerMediaSessionJoin
    ) -> bool:
        is_set_as_inactive = True
        streamer_id = streamer_media_session_join.streamer_id
        media_session_id = streamer_media_session_join.media_session_id
        streamer_repository = StreamerRepository(self.db_session)
        media_session_repository = MediaSessionRepository(self.db_session)
        streamer = await streamer_repository.get_one(id=streamer_id)
        media_session = await media_session_repository.get_one(id=media_session_id)
        posts = streamer.posts
        post_media_session_join_repository = PostMediaSessionJoinRepository(
            self.db_session
        )
        for post in posts:
            for media_session_of_post in post.media_sessions:
                if media_session_of_post == media_session:
                    post_media_session_join = (
                        await post_media_session_join_repository.get_one(
                            post_id=post.id, media_session_id=media_session_id
                        )
                    )
                    is_post_media_set_as_inactive = (
                        await post_media_session_join_repository.set_as_inactive(
                            post_media_session_join
                        )
                    )
                    if not is_post_media_set_as_inactive:
                        logging.error(
                            f"Couldn't set as inactive streamer's post-media {media_session_id = }, "
                            f"{streamer_id = }, post_id = {post.id}"
                        )
                        is_set_as_inactive = False
        if is_set_as_inactive:
            streamer_media_session_join.is_active = False
            await self.add(streamer_media_session_join)
        return is_set_as_inactive

    async def set_as_active(
        self, streamer_media_session_join: StreamerMediaSessionJoin
    ) -> bool:
        streamer_media_session_join.is_active = True
        await self.add(streamer_media_session_join)
        return True
