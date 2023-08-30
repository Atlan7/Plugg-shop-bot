import re

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from tgbot.filters.admin import AdminFilter

from tgbot.services.shop_crud import get_sneakers_by_id,  delete_sneakers_by_id
from tgbot.services.image_manager import delete_sneakers_photo 

from tgbot.states.admins.delete_sneakers import DeleteSneakersState

from tgbot.keyboards.users.cancel_keyboard import kb_cancel

delete_sneakers_router = Router()
delete_sneakers_router.message.filter(AdminFilter())


@delete_sneakers_router.message(Command(re.compile(r"delete_sneakers_([0-9]*)")))
async def activate_delete_sneakers_state(
        message: Message, 
        state: FSMContext, 
        session: AsyncSession
    ):
    sneakers_id = int(message.text.split('_')[-1])
    sneakers = await get_sneakers_by_id(sneakers_id, session)

    if sneakers == None:
        await message.answer("Данные кроссовки отсутсвуют.")
    else:
        await state.update_data(get_sneakers=sneakers)
        await state.set_state(DeleteSneakersState.confirmation)

        answers_to_question = ReplyKeyboardBuilder() 
        answers_to_question.add(KeyboardButton(text="Да"))
        answers_to_question.add(KeyboardButton(text="Нет"))
        await message.answer(
            f"Удалить кроссовки {sneakers.name} ?", 
            reply_markup=answers_to_question.as_markup(
                resize_keyboard=True, 
                selective=True, 
                one_time_keyboard=True
            )
        )
        await state.set_state(DeleteSneakersState.confirmation)
        

@delete_sneakers_router.message(
    DeleteSneakersState.confirmation,
    ~(F.text.in_({"Да", "Нет"}))
)
async def process_deleting_sneakers_is_invalid(message: Message):
    return await message.reply("Неверный ответ. Выбери вариант из клавиатуры.")


@delete_sneakers_router.message(DeleteSneakersState.confirmation)
async def confirm_delete_sneakers_state(message: Message, state: FSMContext, session: AsyncSession):
    answer = message.text
    if answer == "Нет": 
        await state.clear()
        await message.answer(
            f"Операция удаления кроссовок была отменена.", 
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        data = await state.get_data()
        sneakers = data["get_sneakers"] 
        delete_sneakers_photo(brand_name=sneakers.brand.name, sneakers_name=sneakers.name)
        await delete_sneakers_by_id(sneakers.id, session)
        await message.answer(f"Кроссовки были успешно удалены.", reply_markup=ReplyKeyboardRemove())
        await state.clear()
