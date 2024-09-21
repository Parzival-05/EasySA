import asyncio
import logging
import threading
from logging.handlers import RotatingFileHandler

from config import CommonConfig
from src.db.models import BaseModel
from src.db.models.engine import engine, db_session
from src.domain.stream_platforms.stream_platform_names import StreamPlatformNames
from src.launch_actor import main as launch_actor_main
from src.launch_bot import main as launch_bot_main
from src.launch_checker import main as launch_checker_main
from src.utils import create_dirs_if_not_exist

module_name = "main"
fh = RotatingFileHandler(
    f"{module_name}.log",
    mode="w",
    encoding="utf-8",
)
logging.basicConfig(
    level=CommonConfig.LOGGER_LEVEL,
    format="%(asctime)s, %(levelname)-8s | %(filename)-23s:%(lineno)-4s | %(threadName)15s: %(message)s",
    handlers=[fh],
)
create_dirs_if_not_exist(
    [
        CommonConfig.STATIC_PATH,
        CommonConfig.POST_PREVIEWS_PATH,
        *[
            f"{CommonConfig.STATIC_PATH}/{stream_platform_name.value}"
            for stream_platform_name in StreamPlatformNames
        ],
    ]
)

BaseModel.metadata.create_all(engine)

if __name__ == "__main__":
    thread1 = threading.Thread(target=asyncio.run, args=(launch_bot_main(db_session),))
    thread2 = threading.Thread(target=launch_actor_main)
    thread3 = threading.Thread(
        target=asyncio.run, args=(launch_checker_main(db_session),)
    )

    threads = [thread1, thread2, thread3]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
