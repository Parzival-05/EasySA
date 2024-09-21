from sqlalchemy import Integer, ForeignKey, Column, Boolean

from src.db.models import BaseIDModel


class StreamerMediaSessionJoin(BaseIDModel):
    __tablename__ = "streamer_media_session_join"
    streamer_id = Column(Integer, ForeignKey("streamers.id"))
    media_session_id = Column(Integer, ForeignKey("media_platform_sessions.id"))
    is_active = Column(Boolean)
