from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.callbacks.brand import BrandCallback

from tgbot.services.shop_crud import edit_brand_name
from tgbot.services.image_manager import rename_img_dir_for_brand
from tgbot.states.admins.edit_brand_name import EditBrandNameState

from tgbot.keyboards.users.cancel_keyboard import kb_cancel

edit_brand_name_router = Router()
edit_brand_name_router.message.filter(AdminFilter())


@edit_brand_name_router.callback_query(
    BrandCallback.filter(F.action == "edit_brand_name"), 
    AdminFilter()
)
async def activate_edit_brand_name_state(
        message: Message, 
        callback_data: BrandCallback, 
        state: FSMContext, 
        bot: Bot
    ):
    await state.set_state(EditBrandNameState.get_old_name)
    await state.update_data(get_old_name=callback_data.brand) 
    await bot.send_message(
        message.from_user.id,
        "Введи новое название для бренда:", 
        reply_markup=kb_cancel
    )
    await state.set_state(EditBrandNameState.get_new_name) 


@edit_brand_name_router.message(EditBrandNameState.get_new_name)
async def get_new_name_for_brand_state(message: Message, state: FSMContext):
    new_name = message.text
    await state.update_data(get_new_name=new_name)

    answers_to_question = ReplyKeyboardBuilder() 
    answers_to_question.add(KeyboardButton(text="Да"))
    answers_to_question.add(KeyboardButton(text="Нет, изменить"))
    answers_to_question.add(KeyboardButton(text="/cancel_process"))
    await message.answer(
        "Хорошо, сохранить название бренда?", 
        reply_markup=answers_to_question.as_markup(
        resize_keyboard=True, 
        selective=True, 
        one_time_keyboard=True
        )
    )
    await state.set_state(EditBrandNameState.confirmation)


@edit_brand_name_router.message(
    EditBrandNameState.confirmation,
    ~(F.text.in_({"Да", "Нет, изменить"}))
)
async def process_editing_brand_name_is_invalid(message: Message):
    return await message.reply("Неверный ответ. Выбери вариант из клавиатуры.")


@edit_brand_name_router.message(EditBrandNameState.confirmation)
async def confirm_new_brand_name_state(
        message: Message, 
        state: FSMContext, 
        session: AsyncSession
    ):
    answer = message.text
    if answer == "Нет, изменить": 
        await state.set_state(EditBrandNameState.get_new_name)
        await message.answer(
            "Введи новое название для бренда:", 
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        data = await state.get_data()
        rename_img_dir_for_brand(data["get_old_name"], data["get_new_name"])
        await edit_brand_name(data["get_old_name"], data["get_new_name"], session)
        await message.answer(
            f"Название бренда было успешно изменено.", 
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
