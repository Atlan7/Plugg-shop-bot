from aiogram.fsm.state import State, StatesGroup


class EditSneakersNameState(StatesGroup):
    get_sneakers = State()
    get_new_name = State()
    confirmation = State()
