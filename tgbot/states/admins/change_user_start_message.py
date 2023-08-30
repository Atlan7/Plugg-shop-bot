from aiogram.fsm.state import State, StatesGroup


class ChangeUserStartMessageState(StatesGroup):
    get_new_message = State()
    confirmation = State()
