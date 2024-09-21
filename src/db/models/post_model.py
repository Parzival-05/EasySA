from typing import Optional, TYPE_CHECKING

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
    preview: Mapped[Optional["PreviewModel"]] = relationship(back_populates="post")
    buttons_info: Mapped[Optional["ButtonsInfoModel"]] = relationship(
        back_populates="post"
    )
    is_active = Column(Boolean)

    streamer_id: Mapped[int] = mapped_column(ForeignKey("streamers.id"))
    streamer: Mapped["StreamerModel"] = relationship(back_populates="posts")
    media_sessions: Mapped[list["MediaSessionModel"]] = relationship(
        back_populates="posts",
        secondary="post_media_session_join",
    )
    published_posts: Mapped[list["PublishedPostModel"]] = relationship(
        back_populates="post"
    )


class PreviewModel(BaseIDModel):
    __tablename__ = "previews"
    # title = Column(String)
    file_path = Column(String)
    post_id: Mapped[Optional[int]] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["PostModel"] = relationship(back_populates="preview")


class ButtonsInfoModel(BaseIDModel):
    __tablename__ = "buttons_infos"
    buttons_info = Column(String)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["PostModel"] = relationship(back_populates="buttons_info")


class PublishedPostModel(BaseModel):
    __tablename__ = "published_posts"
    id = Column(Integer, primary_key=True)
    stream_id = Column(Integer)
    post_id = mapped_column(ForeignKey("posts.id"))
    post: Mapped["PostModel"] = relationship(back_populates="published_posts")
    media_session_id = mapped_column(ForeignKey("media_platform_sessions.id"))
    media_session: Mapped["MediaSessionModel"] = relationship(
        back_populates="published_posts"
    )
    timestamp = Column(DateTime, server_default=func.now())
