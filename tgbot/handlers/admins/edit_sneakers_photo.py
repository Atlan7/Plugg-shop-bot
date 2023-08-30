import re

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from tgbot.filters.admin import AdminFilter

from tgbot.services.shop_crud import get_sneakers_by_id, edit_sneakers_name
from tgbot.services.image_manager import download_sneakers_photo 

from tgbot.states.admins.edit_sneakers_photo import EditSneakersPhotoState

from tgbot.keyboards.users.cancel_keyboard import kb_cancel

edit_sneakers_photo_router = Router()
edit_sneakers_photo_router.message.filter(AdminFilter())


@edit_sneakers_photo_router.message(Command(re.compile(r"edit_photo_([0-9]*)")))
async def activate_edit_sneakers_photo_state(
        message: Message, 
        state: FSMContext, 
        session: AsyncSession
    ):
    sneakers_id = int(message.text.split('_')[-1])
    sneakers = await get_sneakers_by_id(sneakers_id, session) 

    if sneakers == None:
        await message.answer("Данные кроссовки отсутсвуют.")
    else:
        await state.set_state(EditSneakersPhotoState.get_sneakers)
        await state.update_data(get_sneakers=sneakers)
        await message.answer("Пришли новое фото для кроссовок:", reply_markup=kb_cancel)
        await state.set_state(EditSneakersPhotoState.get_new_photo)
    

@edit_sneakers_photo_router.message(EditSneakersPhotoState.get_new_photo, F.photo)
async def get_new_photo_for_sneakers_state(message: Message, state: FSMContext):
    new_photo = message.photo[-1]
    await state.update_data(get_new_photo=new_photo)

    answers_to_question = ReplyKeyboardBuilder() 
    answers_to_question.add(KeyboardButton(text="Да"))
    answers_to_question.add(KeyboardButton(text="Нет, изменить"))
    answers_to_question.row(KeyboardButton(text="/cancel_process"))
    await message.answer(
        "Хорошо, сохранить новую фотографию кроссовок?", 
        reply_markup=answers_to_question.as_markup(
            resize_keyboard=True, 
            selective=True, 
            one_time_keyboard=True
        )
    )
    await state.set_state(EditSneakersPhotoState.confirmation)


@edit_sneakers_photo_router.message(
    EditSneakersPhotoState.confirmation,
    ~(F.text.in_({"Да", "Нет, изменить"}))
)
async def process_editing_brand_photo_is_invalid(message: Message):
    return await message.reply("Неверный ответ. Выбери вариант из клавиатуры.")


@edit_sneakers_photo_router.message(EditSneakersPhotoState.confirmation)
async def confirm_new_sneakers_photo_state(
        message: Message, 
        bot: Bot, 
        state: FSMContext, 
        session: AsyncSession
    ):
    answer = message.text
    if answer == "Нет, изменить": 
        await state.set_state(EditSneakersPhotoState.get_new_photo)
        await message.answer("Пришли новое фото для кроссовок:", reply_markup=kb_cancel)
    else:
        data = await state.get_data()
        data["brand_name"] = data["get_sneakers"].brand.name
        data["sneakers_name"] = data["get_sneakers"].name
        await download_sneakers_photo(data["get_new_photo"], bot, data)
        await message.answer(
            "Фото кроссовок было успешно изменено.", 
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
