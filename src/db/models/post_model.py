from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime, func, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.db.models import BaseIDModel, BaseModel

if TYPE_CHECKING:
    from src.db.models.media_model import MediaSessionModel
    from src.db.models.streamer_model import StreamerModel


class PostModel(BaseIDModel):
    __tablename__ = "posts"
    name = Column(String)
    text = Column(String)
    preview: Mapped["PreviewModel"] = relationship(back_populates="post", cascade="all, delete", uselist=False)
    buttons_info: Mapped["ButtonsInfoModel"] = relationship(
        back_populates="post", cascade="all, delete"
    )
    is_active = Column(Boolean)

    streamer_id: Mapped[int] = mapped_column(ForeignKey("streamers.id", ondelete="CASCADE"))
    streamer: Mapped["StreamerModel"] = relationship(back_populates="posts")
    media_sessions: Mapped[list["MediaSessionModel"]] = relationship(
        back_populates="posts",
        secondary="post_media_session_join",
        cascade="all, delete"
    )
    published_posts: Mapped[list["PublishedPostModel"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )


class PreviewModel(BaseIDModel):
    __tablename__ = "previews"
    file_path = Column(String, nullable=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    post: Mapped["PostModel"] = relationship(back_populates="preview", single_parent=True)


class ButtonsInfoModel(BaseIDModel):
    __tablename__ = "buttons_infos"
    buttons_info = Column(String, nullable=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    post: Mapped["PostModel"] = relationship(back_populates="buttons_info", single_parent=True)


class PublishedPostModel(BaseModel):
    __tablename__ = "published_posts"
    id = Column(Integer, primary_key=True)
    stream_id = Column(Integer)
    post_id = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    post: Mapped["PostModel"] = relationship(back_populates="published_posts")
    media_session_id = mapped_column(ForeignKey("media_platform_sessions.id", ondelete="CASCADE"))
    media_session: Mapped["MediaSessionModel"] = relationship(
        back_populates="published_posts"
    )
    timestamp = Column(DateTime, server_default=func.now())
