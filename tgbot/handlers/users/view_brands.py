from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData 
from aiogram.types import Message, CallbackQuery

from tgbot.filters.user import UserFilter

from tgbot.keyboards.callbacks.buttons_pagination import ButtonsPaginationCallback
from tgbot.services.pagination import (
    send_paginated_inline_keyboard_for_brands,
    send_previous_page,
    send_next_page
)

view_brands_router = Router()
view_brands_router.message.filter(UserFilter())


@view_brands_router.message(Command('brands'), UserFilter())
async def show_list_of_brands(message: Message, bot: Bot, session: AsyncSession):
    await send_paginated_inline_keyboard_for_brands(
        message=message,
        bot=bot,
        session=session,
    )


@view_brands_router.callback_query(
    ButtonsPaginationCallback.filter(F.action == "get_previous_page"), 
    UserFilter()
)
async def get_previous_page(
        callback_query: CallbackQuery, 
        callback_data: ButtonsPaginationCallback, 
        session: AsyncSession
    ):
    await send_previous_page(
        callback_query=callback_query,
        callback_data=callback_data,
        session=session,
    )


@view_brands_router.callback_query(
    ButtonsPaginationCallback.filter(F.action == "get_next_page"), 
    UserFilter()
)
async def get_next_page(
        callback_query: CallbackQuery, 
        callback_data: ButtonsPaginationCallback, 
        session: AsyncSession
    ):
    await send_next_page(
        callback_query=callback_query,
        callback_data=callback_data,
        session=session,
    )
