from enum import StrEnum


class FormPostButtonButtons(StrEnum):
    ADD_NAME = "Добавить текст"
    ADD_URL = "Добавить ссылку"


class EditButtonOfPostButtons(StrEnum):
    EDIT_NAME = "Изменить текст"
    EDIT_URL = "Изменить ссылку"
    DELETE = "Удалить кнопку"


class EditButtonsOfPostButtons(StrEnum):
    ADD_BUTTON = "Добавить кнопку"
