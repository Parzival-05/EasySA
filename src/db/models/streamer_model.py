from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.db.models import BaseIDModel
from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)

if TYPE_CHECKING:
    from src.db.models.media_model import MediaSessionModel
    from src.db.models.platform_model import StreamPlatformModel
    from src.db.models.post_model import PostModel, PublishedPostModel


class StreamerModel(BaseIDModel):
    __tablename__ = "streamers"
    name = Column(String)
    stream_platform_name: Mapped[StreamPlatformNames] = mapped_column(
        ForeignKey("stream_platforms.name")
    )
    stream_platform: Mapped["StreamPlatformModel"] = relationship(
        back_populates="streamers"
    )
    profile_id = Column(String)
    media_sessions: Mapped[list["MediaSessionModel"]] = relationship(
        back_populates="streamers", secondary="streamer_media_session_join"
    )
    posts: Mapped[list["PostModel"]] = relationship(back_populates="streamer")
    is_active = Column(Boolean)
