from math import ceil

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.callbacks.brand import BrandCallback
from tgbot.keyboards.callbacks.buttons_pagination import ButtonsPaginationCallback


def create_inline_buttons_pagination_for_brands(
        buttons: list[InlineKeyboardButton], 
        current_page: int = 1,
        buttons_per_col: int = 8,
        buttons_per_row: int = 1
    ) -> InlineKeyboardBuilder:

    buttons_per_page = buttons_per_col*buttons_per_row 
    total_pages = ceil(len(buttons)/(buttons_per_page))
    markup = InlineKeyboardBuilder()

    start_pos = (current_page-1)*buttons_per_page 
    end_pos = start_pos+buttons_per_page 
    markup.row(*buttons[start_pos:end_pos], width=buttons_per_row)

    previous_page_btn = InlineKeyboardButton(
        text=f"\U00002b05", # :arrow_left: 
        callback_data=ButtonsPaginationCallback(
            action="get_previous_page",
            total_pages=total_pages,
            current_page=current_page,
            buttons_per_col=buttons_per_col,
            buttons_per_row=buttons_per_row,
            buttons_action=BrandCallback.unpack(
                buttons[0].callback_data
            ).action
        ).pack()
    ) 
    current_page_btn = InlineKeyboardButton(
        text=f"{current_page}/{total_pages}", 
        callback_data="page_{current_page}"
    )
    next_page_btn = InlineKeyboardButton(
        text=f"\U000027a1", # :arrow_right:
        callback_data=ButtonsPaginationCallback(
            action="get_next_page",
            total_pages=total_pages,
            current_page=current_page,
            buttons_per_col=buttons_per_col,
            buttons_per_row=buttons_per_row,
            buttons_action=BrandCallback.unpack(
                buttons[0].callback_data
            ).action
        ).pack()
    )

    if current_page == 1:
        markup.row(
            current_page_btn,
            next_page_btn
        )
    elif total_pages > current_page:
        markup.row(
            previous_page_btn,
            current_page_btn,
            next_page_btn,
        )
    else:
        markup.row(
            previous_page_btn,
            current_page_btn
        )

    return markup.as_markup()
