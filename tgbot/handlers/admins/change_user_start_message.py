from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from aiogram.exceptions import TelegramBadRequest

from tgbot.filters.admin import AdminFilter

from tgbot.states.admins.change_user_start_message import ChangeUserStartMessageState
from tgbot.services.start_message_manager import set_user_start_message

from tgbot.keyboards.users.cancel_keyboard import kb_cancel

change_user_start_message_router = Router()
change_user_start_message_router.message.filter(AdminFilter())


@change_user_start_message_router.message(Command("change_user_start_message"), AdminFilter())
async def activate_edit_brand_name_state(message: Message, state: FSMContext):
    await message.answer(
        "Введи новое стартовое сообщение для пользователей:", 
        reply_markup=kb_cancel
    )
    await state.set_state(ChangeUserStartMessageState.get_new_message)


@change_user_start_message_router.message(ChangeUserStartMessageState.get_new_message)
async def get_new_name_for_brand_state(message: Message, state: FSMContext):
    new_message = message.text

    answers_to_question = ReplyKeyboardBuilder() 
    answers_to_question.add(KeyboardButton(text="Да"))
    answers_to_question.add(KeyboardButton(text="Нет, изменить"))
    answers_to_question.add(KeyboardButton(text="/cancel_process"))
    try:
        await message.answer(
            new_message,
            parse_mode="HTML"
        )
    except TelegramBadRequest as err:
        await message.answer(
            f"В данном сообщении присутвуют теги, которые не поддерживает telegram:\n{err}"
        )
        await state.set_state(ChangeUserStartMessageState.get_new_message)
        await message.answer(
            "Введи новое стартовое сообщение для пользователей:", 
            reply_markup=kb_cancel
        )
    else:
        await message.answer(
            "Хорошо, cохранить новое стартовое сообщение для пользователей?", 
            reply_markup=answers_to_question.as_markup(
                resize_keyboard=True, 
                selective=True, 
                one_time_keyboard=True
            )
        )
        await state.update_data(get_new_message=new_message)
        await state.set_state(ChangeUserStartMessageState.confirmation)


@change_user_start_message_router.message(
    ChangeUserStartMessageState.confirmation,
    ~(F.text.in_({"Да", "Нет, изменить"}))
)
async def process_editing_user_start_message_is_invalid(message: Message):
    return await message.reply("Неверный ответ. Выбери вариант из клавиатуры.")


@change_user_start_message_router.message(ChangeUserStartMessageState.confirmation)
async def confirm_new_brand_name_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == "Нет, изменить": 
        await state.set_state(ChangeUserStartMessageState.get_new_message)
        await message.answer(
            "Введи новое стартовое сообщение для пользователей:", 
            reply_markup=kb_cancel
        )
    else:
        data = await state.get_data()
        set_user_start_message(new_message=data["get_new_message"])
        await message.answer(
            f"Стартовое сообщение было успешно изменено.", 
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
