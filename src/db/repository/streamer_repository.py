from src.db.models.streamer_model import StreamerModel
from src.db.repository.base_repository import Repository


class StreamerRepository(Repository):
    MODEL = StreamerModel

    async def get_active_streamers(self):
        return await self.list(is_active=True)

    async def set_as_active(self, streamer: StreamerModel) -> bool:
        can_set_as_active = False
        for post in streamer.posts:
            if post.is_active:
                can_set_as_active = True
                break
        if can_set_as_active:
            streamer.is_active = True
            await self.add(streamer)
        return can_set_as_active

    async def set_as_inactive(self, streamer: StreamerModel) -> bool:
        streamer.is_active = False
        await self.add(streamer)
        return True
