from aiogram import Bot
from aiogram.filters.callback_data import CallbackData 
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton

from tgbot.keyboards.users.pagination import create_inline_buttons_pagination_for_brands
from tgbot.keyboards.callbacks.buttons_pagination import ButtonsPaginationCallback
from tgbot.keyboards.admins.buttons_for_brands import (
    create_buttons_for_brands as admin_buttons_for_brands 
)
from tgbot.keyboards.users.buttons_for_brands import (
    create_buttons_for_brands as user_buttons_for_brands
)

from sqlalchemy.ext.asyncio import AsyncSession

from .shop_crud import get_all_brands


async def send_paginated_inline_keyboard_for_brands(
        message: Message, 
        bot: Bot, 
        session: AsyncSession,
        is_admin: bool = False,
        buttons_action: str = "show_sneakers_of_brand"
    ):
    brands = await get_all_brands(session)
    if len(brands) == 0: 
        await message.answer(f"Бренды отсутвуют.") 
    else:
        if is_admin:
            buttons = admin_buttons_for_brands(brands, action=buttons_action)
            pagination = create_inline_buttons_pagination_for_brands(buttons, buttons_per_row=3)
        else:
            buttons = user_buttons_for_brands(brands, action=buttons_action)
            pagination = create_inline_buttons_pagination_for_brands(buttons)

        await message.answer("Список брендов:" , reply_markup=pagination)


async def send_previous_page(
        callback_query: CallbackQuery, 
        callback_data: ButtonsPaginationCallback, 
        session: AsyncSession,
        is_admin: bool = False
    ):
    if callback_data.current_page > 1: 
        brands = await get_all_brands(session)

        if is_admin:
            buttons = admin_buttons_for_brands(brands, action=callback_data.buttons_action)
        else:
            buttons = user_buttons_for_brands(brands, action=callback_data.buttons_action)

        pagination = create_inline_buttons_pagination_for_brands(
            buttons, 
            current_page=callback_data.current_page-1, 
            buttons_per_row=callback_data.buttons_per_row
        )
        await callback_query.message.edit_reply_markup(text="Список брендов:" , reply_markup=pagination)


async def send_next_page(
        callback_query: CallbackQuery, 
        callback_data: ButtonsPaginationCallback, 
        session: AsyncSession,
        is_admin: bool = False,
    ):
    if callback_data.current_page < callback_data.total_pages: 
        brands = await get_all_brands(session)

        if is_admin:
            buttons = admin_buttons_for_brands(brands, action=callback_data.buttons_action)
        else:
            buttons = user_buttons_for_brands(brands, action=callback_data.buttons_action)

        pagination = create_inline_buttons_pagination_for_brands(
            buttons, 
            current_page=callback_data.current_page+1, 
            buttons_per_row=callback_data.buttons_per_row
        )
        await callback_query.message.edit_reply_markup(text="Список брендов:" , reply_markup=pagination)
