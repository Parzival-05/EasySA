from sqlalchemy import Column, Integer, ForeignKey, Boolean

from src.db.models import BaseIDModel


class PostMediaSessionJoin(BaseIDModel):
    __tablename__ = "post_media_session_join"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    media_session_id = Column(
        Integer, ForeignKey("media_platform_sessions.id", ondelete="CASCADE")
    )
    is_active = Column(Boolean)
