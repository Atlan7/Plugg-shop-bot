from aiogram.fsm.state import State, StatesGroup


class EditSneakersPhotoState(StatesGroup):
    get_sneakers = State()
    get_new_photo = State()
    confirmation = State()
