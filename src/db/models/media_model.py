from typing import TYPE_CHECKING

from sqlalchemy import String, Column, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db.models.streamer_model import StreamerModel
from src.domain.media_platforms.media_names import MediaPlatformNames

from src.db.models import BaseIDModel, BaseModel

if TYPE_CHECKING:
    from src.db.models.post_model import PostModel, PublishedPostModel


class MediaPlatformModel(BaseModel):
    __tablename__ = "media_platforms"
    name = Column(Enum(MediaPlatformNames), primary_key=True)
    media_sessions: Mapped[list["MediaSessionModel"]] = relationship(
        back_populates="media_platform", cascade="all, delete-orphan"
    )


class MediaSessionModel(BaseIDModel):
    __tablename__ = "media_platform_sessions"
    name = Column(String)
    media_name: Mapped[MediaPlatformNames] = mapped_column(
        ForeignKey("media_platforms.name")
    )
    media_platform: Mapped["MediaPlatformModel"] = relationship(
        back_populates="media_sessions"
    )
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    extra_field = Column(String, nullable=True)
    expires_in = Column(DateTime, nullable=True)
    is_active = Column(Boolean)

    streamers: Mapped[list["StreamerModel"]] = relationship(
        back_populates="media_sessions", secondary="streamer_media_session_join", cascade="all, delete"
    )
    posts: Mapped[list["PostModel"]] = relationship(
        back_populates="media_sessions", secondary="post_media_session_join", cascade="all, delete"
    )
    published_posts: Mapped[list["PublishedPostModel"]] = relationship(
        back_populates="media_session", cascade="all, delete-orphan"
    )
