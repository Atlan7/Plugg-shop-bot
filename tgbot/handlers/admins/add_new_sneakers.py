from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram.filters.callback_data import CallbackData 

from tgbot.states.admins.add_new_sneakers import AddNewSneakersState
from tgbot.keyboards.users.cancel_keyboard import kb_cancel
from tgbot.filters.admin import AdminFilter
from tgbot.services import (
    shop_crud, 
    image_manager,
    pagination
)

from tgbot.keyboards.admins.buttons_for_brands import create_buttons_for_brands 
from tgbot.keyboards.callbacks.brand import BrandCallback

add_new_sneakers_router = Router()
add_new_sneakers_router.message.filter(AdminFilter())


@add_new_sneakers_router.message(Command('add_new_sneakers'))
async def activate_add_new_sneakers_state(
        message: Message, 
        bot: Bot, 
        state: FSMContext, 
        session: AsyncSession
    ):
    await message.answer("Выбери бренд для кроссовок.", reply_markup=kb_cancel)
    await state.set_state(AddNewSneakersState.brand_name)
    await pagination.send_paginated_inline_keyboard_for_brands(
        message=message,
        bot=bot,
        session=session,
        is_admin=True,
        buttons_action="select_brand"
    )


@add_new_sneakers_router.callback_query(
    AddNewSneakersState.brand_name,
    BrandCallback.filter(F.action == "select_brand")
)
async def select_sneakers_brand_state(
        callback_query: CallbackQuery, 
        callback_data: CallbackData, 
        bot: Bot,
        session: AsyncSession, 
        state: FSMContext
    ):
    brand = callback_data.brand

    await state.update_data(brand_name=brand)
    await bot.send_message(
        callback_query.message.chat.id, 
        'Отлично, введи название кроссовок:'
    )
    await state.set_state(AddNewSneakersState.sneakers_name)


@add_new_sneakers_router.message(AddNewSneakersState.sneakers_name)
async def set_name_for_sneakers_state(
        message: Message, 
        session: AsyncSession, 
        state: FSMContext
    ):
    sneakers_name = message.text
    data = await state.get_data()

    result = await shop_crud.get_sneakers_by_name_and_brand(
        sneakers_name, 
        data["brand_name"], 
        session
    )
    if result != None:
        await message.answer(f"Данное название уже присутвует, выбери другое:")
        await state.set_state(AddNewSneakersState.sneakers_name)
    else:
        await state.update_data(sneakers_name=sneakers_name)
        await message.answer(f'Укажи стоимость кроссовок:')
        await state.set_state(AddNewSneakersState.sneakers_price)


@add_new_sneakers_router.message(AddNewSneakersState.sneakers_price)
async def set_price_for_sneakers_state(message: Message, state: FSMContext):
    sneakers_price = message.text
    if sneakers_price.isdigit():
        sneakers_price = int(sneakers_price)
        if sneakers_price <= 0:
            await message.answer(f'Стоимость кроссовок должна быть больше нуля.')
            await message.answer("Введи стоимость кроссовок:", reply_markup=kb_cancel)
            await state.set_state(AddNewSneakersState.sneakers_price)
        else:
            await state.update_data(sneakers_price=sneakers_price)
            await message.answer(f'Теперь пришли мне фотографию кроссовок.')
            await state.set_state(AddNewSneakersState.sneakers_photo)
    else:
        await message.answer(f'Стоимость кроссовок должна быть положительным числом.')
        await state.set_state(AddNewSneakersState.sneakers_price)


@add_new_sneakers_router.message(
    AddNewSneakersState.sneakers_photo, 
    F.photo == None
)
async def process_get_image_for_sneakers_is_invalid(message: Message):
    return await message.reply("Пришли мне фотографию кроссовок.")


@add_new_sneakers_router.message(AddNewSneakersState.sneakers_photo, F.photo)
async def set_name_for_sneakers_state(
        message: Message, 
        session: AsyncSession, 
        state: FSMContext,
        bot: Bot
    ):
    data = await state.get_data()

    await shop_crud.add_new_sneakers(
        brand_name=data["brand_name"],
        name=data["sneakers_name"],
        price=data["sneakers_price"],
        session=session
    )

    await image_manager.download_sneakers_photo(message.photo[-1], bot, data)
    await message.answer('Кроссовки были успешно добавлены!')
    await state.clear()
