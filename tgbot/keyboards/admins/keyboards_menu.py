from aiogram import types 
from aiogram.utils.keyboard import ReplyKeyboardBuilder


kb = [
        [types.KeyboardButton(text="/add_new_brand")],
        [types.KeyboardButton(text="/add_new_sneakers")]
    ]

kb_menu = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
)
