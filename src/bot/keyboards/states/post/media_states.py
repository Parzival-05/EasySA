from aiogram.fsm.state import StatesGroup, State


class AddMediaState(StatesGroup):
    SELECT_PLATFORM = State()
    ADD_NAME = State()
    ADD_CREDS = State()
