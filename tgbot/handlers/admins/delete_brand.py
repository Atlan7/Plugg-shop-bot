from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router, F, Bot
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.callbacks.brand import BrandCallback

from tgbot.services.shop_crud import delete_brand_by_name
from tgbot.services.image_manager import delete_brand_images

from tgbot.states.admins.delete_brand import DeleteBrandState

delete_brand_router = Router()
delete_brand_router.message.filter(AdminFilter())


@delete_brand_router.callback_query(
    BrandCallback.filter(F.action == "delete_brand"), 
    AdminFilter()
)
async def activate_delete_brand_state(
        callback_query: CallbackQuery, 
        callback_data: BrandCallback, 
        state: FSMContext, 
        bot: Bot
    ):
    await state.set_state(DeleteBrandState.get_name)
    await state.update_data(get_name=callback_data.brand) 

    answers_to_question = ReplyKeyboardBuilder() 
    answers_to_question.add(KeyboardButton(text="Да"))
    answers_to_question.add(KeyboardButton(text="Нет"))
    await bot.send_message(
        callback_query.from_user.id,
        f"Удалить бренд '{callback_data.brand}'? Вместе с ним удалятся все кроссовки.", 
        reply_markup=answers_to_question.as_markup(
            resize_keyboard=True, 
            selective=True, 
            one_time_keyboard=True,
            show_alert=True
        )
    )
    await state.set_state(DeleteBrandState.confirmation)


@delete_brand_router.message(
    DeleteBrandState.confirmation,
    ~(F.text.in_({"Да", "Нет"}))
)
async def process_editing_brand_name_is_invalid(message: Message):
    return await message.reply("Неверный ответ. Выбери вариант из клавиатуры.")


@delete_brand_router.message(DeleteBrandState.confirmation)
async def confirm_brand_deletion_state(
        message: Message, 
        state: FSMContext, 
        session: AsyncSession
    ):
    answer = message.text
    if answer == "Нет": 
        await state.clear()
        await message.answer(
            f"Операция удаления была отменена.", 
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        data = await state.get_data()
        brand_name = data["get_name"] 
        await delete_brand_by_name(brand_name, session)
        delete_brand_images(brand_name)
        await message.answer(
            f"Бренд '{brand_name}' был успешно удалён.", 
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
