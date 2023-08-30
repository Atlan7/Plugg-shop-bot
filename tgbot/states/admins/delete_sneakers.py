from aiogram.fsm.state import State, StatesGroup


class DeleteSneakersState(StatesGroup):
    get_sneakers = State()
    confirmation = State()
