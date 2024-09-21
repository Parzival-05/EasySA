from enum import StrEnum


class PostButtons(StrEnum):
    GET_LIST = "Список постов"
    ADD = "Добавить пост"


class PostActionButtons(StrEnum):
    EDIT_MEDIA = "Изменить медиа"
    EDIT_NAME = "Изменить имя"
    EDIT_TEXT = "Изменить сообщение"
    DELETE = "Удалить пост"
    SET_AS_ACTIVE = "Сделать активным"
    SET_AS_INACTIVE = "Сделать неактивным"
