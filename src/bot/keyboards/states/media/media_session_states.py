from aiogram.fsm.state import StatesGroup, State


class EditMediaSessionState(StatesGroup):
    EDIT_NAME = State()
