from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile

from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.filters.admin import AdminFilter

from tgbot.keyboards.callbacks.brand import BrandCallback

from tgbot.services.view_sneakers_of_brand import send_sneakers_photo

view_sneakers_of_brand_router = Router()
view_sneakers_of_brand_router.message.filter(AdminFilter())


@view_sneakers_of_brand_router.callback_query(
    BrandCallback.filter(F.action == "show_sneakers_of_brand"), 
    AdminFilter()
)
async def show_sneakers_of_brand(
        callback_query: CallbackQuery, 
        callback_data: BrandCallback, 
        session: AsyncSession,
        bot: Bot
    ):
    await send_sneakers_photo(
        callback_query=callback_query, 
        callback_data=callback_data, 
        session=session, 
        bot=bot, 
        is_admin=True
    )
