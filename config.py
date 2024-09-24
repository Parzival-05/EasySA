import logging


class CommonConfig:
    ENV_PATH = ".env"
    STATIC_PATH = "static/"
    POST_PREVIEWS_PATH = STATIC_PATH + "posts/"
    LOGGER_LEVEL = logging.INFO
    DB_URL = "sqlite:///db.sqlite3"


class AppConfig:
    PORT = 8000
    LOOP_TIMEOUT = 10  # seconds
    REQUESTS_TIMEOUT = 0.1


class ActorConfig:
    PORT = 35000
