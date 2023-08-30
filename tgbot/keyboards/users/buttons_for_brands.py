from typing import Any, Optional

from aiogram.filters.callback_data import CallbackData 

from aiogram.types import InlineKeyboardButton

from tgbot.models.shop import Brand

from tgbot.keyboards.callbacks.brand import BrandCallback


def create_buttons_for_brands(brands: list[Brand], action="show_sneakers_of_brand") -> list[InlineKeyboardButton]:
    buttons = [ 
        InlineKeyboardButton(
            text=brand.name, 
            callback_data=BrandCallback(
                action=action, brand=f"{brand.name}").pack(),       
        )
        for brand in brands
    ]
    return buttons
