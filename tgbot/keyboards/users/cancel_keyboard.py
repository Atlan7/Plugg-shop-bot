from aiogram import types 
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from aiogram.filters.callback_data import CallbackData 


kb = [
        [types.KeyboardButton(text="/cancel_process")],
]

kb_cancel = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
)
