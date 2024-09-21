from src.db.models.post_model import (
    PostModel,
    PreviewModel,
    ButtonsInfoModel,
    PublishedPostModel,
)
from src.db.repository.base_repository import Repository


class PostRepository(Repository):
    MODEL = PostModel

    async def get_posts_of_streamer(self, streamer_id: int):
        return self.db_session.query(PostModel).filter_by(streamer_id=streamer_id).all()

    async def set_as_active(self, post: PostModel) -> bool:
        from src.db.repository.association.post_media_repository import (
            PostMediaSessionJoinRepository,
        )

        post_media_session_join_repository = PostMediaSessionJoinRepository(
            self.db_session
        )
        can_set_as_active = False
        for media_session in post.media_sessions:
            post_media_session_join = await post_media_session_join_repository.get_one(
                post_id=post.id, media_session_id=media_session.id
            )
            if post_media_session_join.is_active:
                can_set_as_active = True
                break
        if can_set_as_active:
            post.is_active = True
            await self.add(post)
        return can_set_as_active

    async def set_as_inactive(self, post: PostModel) -> bool:
        post.is_active = False
        streamer_posts = post.streamer.posts
        for streamer_post in streamer_posts:
            if streamer_post.is_active and streamer_post != post:
                break
        else:
            post.streamer.is_active = False
        await self.add(post)
        return True


class PreviewRepository(Repository):
    MODEL = PreviewModel


class ButtonsInfoRepository(Repository):
    MODEL = ButtonsInfoModel


class PublishedPostRepository(Repository):
    MODEL = PublishedPostModel
