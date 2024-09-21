from aiogram.fsm.state import StatesGroup, State


class EditStreamerState(StatesGroup):
    EDIT_NAME = State()
    EDIT_ACTIVE_POST = State()
    EDIT_ACTIVITY = State()
    CONFIRM_DELETION = State()


class AddStreamerState(StatesGroup):
    GET_NAME = State()
    CHOOSE_PLATFORM = State()
    GET_PROFILE = State()
