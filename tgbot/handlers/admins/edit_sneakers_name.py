import re

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from tgbot.filters.admin import AdminFilter

from tgbot.services.shop_crud import (
    get_sneakers_by_id, 
    edit_sneakers_price, 
    get_sneakers_by_name_and_brand, 
    edit_sneakers_name 
)
from tgbot.states.admins.edit_sneakers_name import EditSneakersNameState

from tgbot.services.image_manager import rename_sneakers_img
from tgbot.keyboards.users.cancel_keyboard import kb_cancel

edit_sneakers_name_router = Router()
edit_sneakers_name_router.message.filter(AdminFilter())


@edit_sneakers_name_router.message(Command(re.compile(r"edit_name_([0-9]*)")))
async def activate_edit_sneakers_name_state(
        message: Message, 
        state: FSMContext, 
        session: AsyncSession
    ):
    sneakers_id = int(message.text.split('_')[-1])
    sneakers = await get_sneakers_by_id(sneakers_id, session) 

    if sneakers == None:
        await message.answer("Данные кроссовки отсутсвуют.")
    else:
        await state.set_state(EditSneakersNameState.get_sneakers)
        await state.update_data(get_sneakers=sneakers)
        await message.answer("Введи новое название для кроссовок:", reply_markup=kb_cancel)
        await state.set_state(EditSneakersNameState.get_new_name)
    

@edit_sneakers_name_router.message(EditSneakersNameState.get_new_name)
async def get_new_name_for_sneakers_state(
        message: Message, 
        state: FSMContext, 
        session: AsyncSession
    ):
    new_name = message.text
    await state.update_data(get_new_name=new_name)

    data = await state.get_data()
    result = await get_sneakers_by_name_and_brand(
        new_name, 
        data["get_sneakers"].brand.name, 
        session
    )
    if result != None:
        await message.answer(f"Данное название уже присутвует, выбери другое:")
        await state.set_state(EditSneakersNameState.get_new_name)
    else:
        answers_to_question = ReplyKeyboardBuilder() 
        answers_to_question.add(KeyboardButton(text="Да"))
        answers_to_question.add(KeyboardButton(text="Нет, изменить"))
        answers_to_question.row(KeyboardButton(text="/cancel_process"))
        await message.answer(
            "Хорошо, сохранить название кроссовок?", 
            reply_markup=answers_to_question.as_markup(
                resize_keyboard=True, 
                selective=True, 
                one_time_keyboard=True
            )
        )
        await state.set_state(EditSneakersNameState.confirmation)


@edit_sneakers_name_router.message(
    EditSneakersNameState.confirmation,
    ~(F.text.in_({"Да", "Нет, изменить"}))
)
async def process_editing_brand_name_is_invalid(message: Message):
    return await message.reply("Неверный ответ. Выбери вариант из клавиатуры.")


@edit_sneakers_name_router.message(EditSneakersNameState.confirmation)
async def confirm_new_sneakers_name_state(
        message: Message, 
        state: FSMContext, 
        session: AsyncSession
    ):
    answer = message.text
    if answer == "Нет, изменить": 
        await state.set_state(EditSneakersNameState.get_new_name)
        await message.answer(
            "Введи новое название для кроссовок:", 
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        data = await state.get_data()
        sneakers = await get_sneakers_by_id(data["get_sneakers"].id, session) 
        rename_sneakers_img(
            sneakers_brand=data["get_sneakers"].brand.name, 
            old_sneakers_name=data["get_sneakers"].name, 
            new_sneakers_name=data["get_new_name"]
        )
        await edit_sneakers_name(sneakers, data["get_new_name"], session)
        await message.answer(
            f"Название кроссовок было успешно изменено.", 
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
