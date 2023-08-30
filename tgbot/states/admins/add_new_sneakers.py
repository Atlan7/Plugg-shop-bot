from aiogram.fsm.state import State, StatesGroup


class AddNewSneakersState(StatesGroup):
    brand_name = State()
    sneakers_name = State()
    sneakers_price = State()
    sneakers_photo = State()
