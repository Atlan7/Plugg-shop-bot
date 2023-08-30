from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from tgbot.filters.admin import AdminFilter

from tgbot.keyboards.admins.keyboards_menu import kb_menu

start_message_router = Router()
start_message_router.message.filter(AdminFilter())


@start_message_router.message(CommandStart(), AdminFilter())
async def start(message: Message):
    await message.answer("Привет, админ!", reply_markup=kb_menu)
