from aiogram import Router, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from tgbot.states.admins.add_new_brand import AddNewBarandState
from tgbot.filters.admin import AdminFilter
from tgbot.services import shop_crud
from tgbot.keyboards.users.cancel_keyboard import kb_cancel

from sqlalchemy.ext.asyncio import AsyncSession

add_new_brand_router = Router()
add_new_brand_router.message.filter(AdminFilter())


@add_new_brand_router.message(Command('add_new_brand'))
async def activate_add_new_brand_state(message: Message, state: FSMContext):
    await message.answer(
        f"Введи название бренда, которое ты хочешь добавить:", 
        reply_markup=kb_cancel
    )
    await state.set_state(AddNewBarandState.get_name)


@add_new_brand_router.message(AddNewBarandState.get_name)
async def get_name_of_the_new_brand_state(
        message: Message, 
        state: FSMContext, 
        session: AsyncSession
    ):
    given_name = message.text
    await state.update_data(get_name=given_name)

    result = await shop_crud.get_brand_by_name(given_name, session)
    if result != None:
        await message.answer(
            f"Данное название уже присутвует, выбери другое:",
            reply_markup=kb_cancel
        )
        await state.set_state(AddNewBarandState.get_name)
    else:
        answers_to_question = ReplyKeyboardBuilder() 
        answers_to_question.add(KeyboardButton(text="Да"))
        answers_to_question.add(KeyboardButton(text="Нет, изменить"))
        answers_to_question.row(KeyboardButton(text="/cancel_process"))
        await message.answer(
            "Хорошо, сохранить название бренда?", 
            reply_markup=answers_to_question.as_markup(
                resize_keyboard=True, 
                selective=True, 
                one_time_keyboard=True
            )
        )
        await state.set_state(AddNewBarandState.confirmation)


@add_new_brand_router.message(
    AddNewBarandState.confirmation,
    ~(F.text.in_({"Да", "Нет, изменить"}))
)
async def process_creating_new_name_is_invalid(message: Message):
    return await message.reply("Неверный ответ. Выбери вариант из клавиатуры.")


@add_new_brand_router.message(AddNewBarandState.confirmation)
async def confirm_new_brand_name_state(
        message: Message, 
        state: FSMContext, 
        session: AsyncSession
    ):
    answer = message.text
    if answer == "Нет, изменить": 
        await state.set_state(AddNewBarandState.get_name)
        await message.answer(
            f"Введи название бренда, которое ты хочешь добавить:", 
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        data = await state.get_data()
        await shop_crud.add_new_brand(data["get_name"], session)
        await message.answer(
            f'Название бренда было успешно добавлено.', 
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
