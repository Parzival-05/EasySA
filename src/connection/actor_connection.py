import logging

from aiogram.client.session import aiohttp

from src.connection.messages import DataMessage
from config import ActorConfig


class ActorConnection:
    @staticmethod
    async def send_message(message: DataMessage):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://127.0.0.1:{ActorConfig.PORT}/send_message",
                json=message.model_dump(),
            ) as resp:
                logging.info(resp.content)
