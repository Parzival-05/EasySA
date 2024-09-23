from sqlalchemy import Column, Integer, ForeignKey, Boolean

from src.db.models import BaseIDModel, BaseModel


class PostMediaSessionJoin(BaseModel):
    __tablename__ = "post_media_session_join"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    media_session_id = Column(
        Integer, ForeignKey("media_platform_sessions.id", ondelete="CASCADE"), primary_key=True
    )
    is_active = Column(Boolean)
