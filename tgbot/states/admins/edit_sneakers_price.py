from aiogram.fsm.state import State, StatesGroup


class EditSneakersPriceState(StatesGroup):
    get_sneakers = State()
    get_new_price = State()
    confirmation = State()
