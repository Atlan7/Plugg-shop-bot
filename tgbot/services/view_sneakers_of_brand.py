from pathlib import Path

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile

from sqlalchemy.ext.asyncio import AsyncSession
from .shop_crud import get_all_sneakers_of_brand

from tgbot.keyboards.callbacks.brand import BrandCallback

from tgbot.models.shop import Sneakers

from tgbot.config import preloaded_config


async def send_sneakers_photo(
        callback_query: CallbackQuery, 
        callback_data: BrandCallback, 
        session: AsyncSession,
        bot: Bot,
        is_admin: bool = False
    ):
    sneakers = await get_all_sneakers_of_brand(callback_data.brand, session)
    len_sneakers = len(sneakers)

    if len_sneakers == 0:
        await bot.send_message(
            callback_query.message.chat.id, 
            text=f"Кроссовки бренда {callback_data.brand} отсутсвуют."
        )
    else:
        await bot.send_message(
            callback_query.message.chat.id, 
            text=f"Кроссовки бренда {callback_data.brand}:"
        )

        base_path = f'{preloaded_config.media.base_path}/{callback_data.brand}'
        photos = list() 
        prepared_photos = 0  
        for sneaker in sneakers:
            caption = get_sneakers_photo_caption(sneaker, is_admin=is_admin)
            photo = InputMediaPhoto(
                media=FSInputFile(f'{base_path}/{sneaker.name}.jpg'), 
                caption=caption, 
                parse_mode="HTML"
            )
            photos.append(photo)
            prepared_photos += 1

            # send_media_group accepts only 10 photos per message, so we send photos partially.
            # (prepared_photos % 10 == 0) - shows what we accumulated 10 photos.
            # (prepared_photos == len_sneakers) - shows what quantity of remaining photots less than 10.
            if (prepared_photos % 10 == 0) or (prepared_photos == len_sneakers):
                await bot.send_media_group(callback_query.message.chat.id, photos)
                photos = list()


def get_sneakers_photo_caption(sneakers: Sneakers, is_admin: bool = False) -> str:
    main_info = f"Название: <strong>{sneakers.name}</strong>\nЦена: <strong>{sneakers.price} руб.</strong>" 

    if is_admin:
        _id = sneakers.id
        options = f"/edit_name_{_id}\n/edit_price_{_id}\n/edit_photo_{_id}\n/delete_sneakers_{_id}"
    else:
        links_to_managers: list[str] = list()
        managers_usernames = preloaded_config.tg_bot.managers_usernames
        for num, username in enumerate(managers_usernames, 1):
            links_to_managers.append(f"<a href='https://telegram.me/{username}'>Написать менеджеру {num}</a>\n")
        options = f"".join(links_to_managers)

    caption = f"{main_info}\n{options}"

    return caption 
