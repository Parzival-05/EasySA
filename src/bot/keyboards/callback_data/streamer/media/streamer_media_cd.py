from src.bot.keyboards.callback_data.media.media_session_cd import BaseMediaSessionCD
from src.bot.keyboards.callback_data.streamer.streamer_cd import (
    BaseStreamerCD,
)
from src.db.models.media_model import MediaSessionModel
from src.db.models.streamer_model import StreamerModel


class BaseStreamerMediaSessionCD(
    BaseMediaSessionCD, BaseStreamerCD, prefix="BaseStreamerMediaSessionCD"
):
    pass


class GetStreamerMediaSessionCD(
    BaseStreamerMediaSessionCD, prefix="GetStreamerMediaSessionCD"
):
    @staticmethod
    def from_model(media_session: MediaSessionModel, streamer: StreamerModel):
        return GetStreamerMediaSessionCD(
            media_session_id=media_session.id, streamer_id=streamer.id
        )


class AddStreamerMediaSessionIntentCD(
    BaseStreamerCD, prefix="AddStreamerMediaSessionIntentCD"
):
    @staticmethod
    def from_model(streamer: StreamerModel):
        return AddStreamerMediaSessionIntentCD(streamer_id=streamer.id)


class AddStreamerMediaSessionCD(
    BaseStreamerMediaSessionCD, prefix="AddStreamerMediaSessionCD"
):
    @staticmethod
    def from_model(media_session: MediaSessionModel, streamer: StreamerModel):
        return AddStreamerMediaSessionCD(
            media_session_id=media_session.id, streamer_id=streamer.id
        )
