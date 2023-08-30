from typing import Any, Optional

from aiogram.filters.callback_data import CallbackData 

from aiogram.types import InlineKeyboardButton

from tgbot.models.shop import Brand

from tgbot.keyboards.callbacks.brand import BrandCallback


def create_buttons_for_brands(brands: list[Brand], action="show_sneakers_of_brand") -> list[InlineKeyboardButton]:
    buttons = list()
    for brand in brands:
        buttons.extend([
            InlineKeyboardButton(
                text=brand.name, 
                callback_data=BrandCallback(
                    action=action, brand=f"{brand.name}").pack(),       
            ),
            InlineKeyboardButton(
                text="\U00002712", 
                callback_data=BrandCallback(
                    action="edit_brand_name", brand=f"{brand.name}").pack()       
            ),
            InlineKeyboardButton(
                text="\U0000274c", 
                callback_data=BrandCallback(
                    action="delete_brand", brand=f"{brand.name}").pack()       
            ),
        ])
    return buttons
