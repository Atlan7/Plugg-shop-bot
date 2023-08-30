from aiogram.fsm.state import State, StatesGroup


class DeleteBrandState(StatesGroup):
    get_name = State()
    confirmation = State()
