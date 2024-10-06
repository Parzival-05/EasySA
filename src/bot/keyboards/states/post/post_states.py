from aiogram.fsm.state import StatesGroup, State


class EditPostState(StatesGroup):
    EDIT_MEDIA = State()
    EDIT_NAME = State()
    EDIT_TEXT = State()
    CONFIRM_DELETION = State()
    EDIT_BUTTONS = State()


class AddPostState(StatesGroup):
    ADD_NAME = State()
    ADD_TEXT = State()
    ADD_CUSTOM_PREVIEW = State()
    ADD_MEDIA = State()
