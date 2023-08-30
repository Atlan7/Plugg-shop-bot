from aiogram.fsm.state import State, StatesGroup


class EditBrandNameState(StatesGroup):
    get_old_name = State()
    get_new_name = State()
    confirmation = State()
