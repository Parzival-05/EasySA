from sqlalchemy import Integer, ForeignKey, Column, Boolean

from src.db.models import BaseModel


class StreamerMediaSessionJoin(BaseModel):
    __tablename__ = "streamer_media_session_join"
    streamer_id = Column(Integer, ForeignKey("streamers.id", ondelete="CASCADE"), primary_key=True)
    media_session_id = Column(Integer, ForeignKey("media_platform_sessions.id", ondelete="CASCADE"), primary_key=True)
    is_active = Column(Boolean)
