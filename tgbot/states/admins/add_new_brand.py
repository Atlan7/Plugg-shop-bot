from aiogram.fsm.state import State, StatesGroup


class AddNewBarandState(StatesGroup):
    get_name = State()
    confirmation = State()
