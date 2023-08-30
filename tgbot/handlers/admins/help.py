from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from tgbot.filters.admin import AdminFilter

from tgbot.keyboards.admins.keyboards_menu import kb_menu

help_message_router = Router()
help_message_router.message.filter(AdminFilter())


@help_message_router.message(Command('help'), AdminFilter())
async def help(message: Message):
    await message.answer("""
Привет, админ!

Доступные команды:

/change_user_start_message - меняет первое сообщение для пользователя, можно использовать HTML теги, но не все работают в телеграмме. (P.S. бот обрабатывает ошибки и покажет какой тег не работает)

/brands - показывает доступные бренды с возможностью редактирования/удаления брендов.
/add_new_brand - позволяет добавлять новые бренды для кроссовок.

/add_new_sneakers - позволяет добавлять новые кроссовки.

Чтобы редактировать/удалить кроссовки надо:
    - нажать /brands и выбрать бренд
    - выбрать фото кроссовок, в описании которых находятся 4 команды: 
        /edit_name_[0-9] - изменение названия кроссовок.
        /edit_price_[0-9] - изменение цены кроссовок.
        /edit_photo_[0-9] - изменение фото кроссовок.
        /delete_sneakers_[0-9] - удаление кроссовок.
        [0-9] - id кроссовок в базе данных.

    - нажать на нужную команду.


/cancel - отменет любой процесс (создание, редактирование, удаление).
    """)
