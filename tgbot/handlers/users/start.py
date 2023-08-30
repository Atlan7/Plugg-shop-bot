from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from tgbot.filters.user import UserFilter

from tgbot.services.start_message_manager import get_user_start_message

start_message_router = Router()


@start_message_router.message(CommandStart(), UserFilter())
async def user_start(message: Message):
    start_message = get_user_start_message() 
    await message.answer(start_message)
