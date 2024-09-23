import asyncio
import logging

from sqlalchemy.orm import Session

from config import AppConfig
from src.checker.checking import Checker
from src.connection.actor_connection import ActorConnection
from src.db.models.all_models import *
from src.db.models.engine import db_session, engine
from src.domain.stream_platforms.sessions.base_platform_session import (
    BaseStreamPlatformSession,
)
from src.domain.stream_platforms.sessions.twitch_session import TwitchSession

BaseModel.metadata.create_all(engine)


async def loop_checking(
        stream_platform_sessions: list[BaseStreamPlatformSession], db_session: Session
):
    checker = Checker(
        db_session=db_session, stream_platform_sessions=stream_platform_sessions
    )
    while True:
        try:
            data_messages = await checker.check_streamers()
            logging.debug(f"{data_messages = }")
            for data_message in data_messages:
                await ActorConnection.send_message(data_message)
            await asyncio.sleep(AppConfig.LOOP_TIMEOUT)
        except Exception as e:
            logging.exception(e)


async def main(db_session: Session):
    stream_platform_sessions = [TwitchSession(db_session)]
    await loop_checking(stream_platform_sessions, db_session)


if __name__ == "__main__":
    asyncio.run(main(db_session))
