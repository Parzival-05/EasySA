from enum import StrEnum


class BaseMenuButtons(StrEnum):
    pass


class StreamerButtons(BaseMenuButtons):
    GET_LIST = "Список стримеров"
    ADD = "Добавить стримера"


class MediaButtons(BaseMenuButtons):
    GET_LIST = "Список медиаплатформ"
    GET_SESSIONS_LIST = "Список медиа"
    ADD = "Добавить медиа"
