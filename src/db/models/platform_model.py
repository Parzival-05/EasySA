from typing import TYPE_CHECKING

from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)

from src.db.models import BaseIDModel, BaseModel

if TYPE_CHECKING:
    from src.db.models.streamer_model import StreamerModel
    from src.db.models.all_models import *


class StreamPlatformModel(BaseModel):
    __tablename__ = "stream_platforms"
    name = Column(Enum(StreamPlatformNames), primary_key=True)
    session: Mapped["StreamPlatformSessionModel"] = relationship(
        back_populates="stream_platform"
    )
    streamers: Mapped[list["StreamerModel"]] = relationship(
        back_populates="stream_platform",
    )


class StreamPlatformSessionModel(BaseIDModel):
    __tablename__ = "stream_platform_sessions"
    stream_platform_name: Mapped[StreamPlatformNames] = mapped_column(
        ForeignKey("stream_platforms.name")
    )
    stream_platform: Mapped["StreamPlatformModel"] = relationship(
        back_populates="session"
    )
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    extra_field = Column(String, nullable=True)
    expires_in = Column(DateTime, nullable=True)
