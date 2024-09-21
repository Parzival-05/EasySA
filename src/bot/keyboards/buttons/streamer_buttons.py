from enum import StrEnum, Enum


class StreamerInfoButtons(Enum):
    """
    Use it to get info about <...> of `StreamerModel`
    """

    STREAMER = "<NOT VISIBLE TO USER>"
    POSTS = "Посты"
    MEDIAS = "Медиа"


class StreamerActionButtons(StrEnum):
    """
    Use it to manipulate with `StreamerModel` instance
    """

    SET_AS_ACTIVE = "Сделать активным"
    SET_AS_INACTIVE = "Сделать неактивным"
    EDIT_NAME = "Изменить имя"
    DELETE = "Удалить стримера"
