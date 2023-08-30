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
        get_sneakers_by_name_and_brand
)
from tgbot.services.image_manager import rename_sneakers_img 
from tgbot.states.admins.edit_sneakers_price import EditSneakersPriceState

from tgbot.keyboards.users.cancel_keyboard import kb_cancel

edit_sneakers_price_router = Router()
edit_sneakers_price_router.message.filter(AdminFilter())


@edit_sneakers_price_router.message(Command(re.compile(r"edit_price_([0-9]*)")))
async def activate_edit_sneakers_price_state(
        message: Message, 
        state: FSMContext, 
        session: AsyncSession
    ):
    sneakers_id = int(message.text.split('_')[-1])
    sneakers = await get_sneakers_by_id(sneakers_id, session) 

    if sneakers == None:
        await message.answer("Данные кроссовки отсутсвуют.")
    else:
        await state.set_state(EditSneakersPriceState.get_sneakers)
        await state.update_data(get_sneakers=sneakers)
        await message.answer("Введи новую стоимость кроссовок:", reply_markup=kb_cancel)
        await state.set_state(EditSneakersPriceState.get_new_price)
    

@edit_sneakers_price_router.message(EditSneakersPriceState.get_new_price)
async def get_new_price_for_sneakers_state(message: Message, state: FSMContext):
    new_price = message.text

    if new_price.isdigit():
        new_price = int(new_price)
        if new_price <= 0:
            await message.answer(f'Стоимость кроссовок должна быть больше нуля.')
            await state.set_state(EditSneakersPriceState.get_new_price)
            await message.answer("Введи стоимость кроссовок:", reply_markup=kb_cancel)
        else:
            await state.update_data(get_new_price=new_price)

            answers_to_question = ReplyKeyboardBuilder() 
            answers_to_question.add(KeyboardButton(text="Да"))
            answers_to_question.add(KeyboardButton(text="Нет, изменить"))
            answers_to_question.row(KeyboardButton(text="/cancel_process"))
            await state.set_state(EditSneakersPriceState.confirmation)
            await message.answer(
                "Хорошо, оставить новую стоимость?", 
                reply_markup=answers_to_question.as_markup(
                resize_keyboard=True, 
                selective=True, 
                one_time_keyboard=True
                )
            )
    else:
        await state.set_state(EditSneakersPriceState.get_new_price)
        await message.answer(
            f'Стоимость кроссовок должна быть положительным числом.\nВведи новую стоимость:'
        )


@edit_sneakers_price_router.message(
    EditSneakersPriceState.confirmation,
    ~(F.text.in_({"Да", "Нет, изменить"}))
)
async def process_editing_brand_name_is_invalid(message: Message):
    return await message.reply("Неверный ответ. Выбери вариант из клавиатуры.")


@edit_sneakers_price_router.message(EditSneakersPriceState.confirmation)
async def confirm_new_sneakers_price_state(message: Message, state: FSMContext, session: AsyncSession):
    answer = message.text
    if answer == "Нет, изменить": 
        await state.set_state(EditSneakersPriceState.get_new_price)
        await message.answer("Введи стоимость кроссовок:", reply_markup=kb_cancel)
    else:
        data = await state.get_data()
        sneakers = await get_sneakers_by_id(data["get_sneakers"].id, session) 
        await edit_sneakers_price(sneakers, data["get_new_price"], session)
        await message.answer(
            f"Стоимость кроссовок была успешно изменена.",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
