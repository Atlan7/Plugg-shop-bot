from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from tgbot.filters.user import UserFilter

from tgbot.keyboards.admins.keyboards_menu import kb_menu

from tgbot.services.start_message_manager import get_user_start_message

help_message_router = Router()


@help_message_router.message(Command('help'), UserFilter())
async def user_help(message: Message):
    await message.answer(f"""
{get_user_start_message()}

Чтобы просмотреть кроссовки надо:
    - нажать на команду /brands.
    - выбрать интересующий бренд кроссовок.

Ссылка для контакта с менеджерами по поводу интересующих кроссовок находится под фото.

    """)
