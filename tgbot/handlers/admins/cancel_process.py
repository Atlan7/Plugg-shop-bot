import logging

from aiogram import F, Router
from aiogram.filters import Command

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from tgbot.filters.admin import AdminFilter

cancel_process_router = Router()
cancel_process_router.message.filter(AdminFilter())


@cancel_process_router.message(Command("cancel_process"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow admin to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await state.set_state(None)
    await message.answer(
        "Процесс отменён.",
        reply_markup=ReplyKeyboardRemove(),
    )
