from aiogram import types
from aiogram.methods.set_my_commands import SetMyCommands


async def set_default_commands(bot):
    commands = [
        types.BotCommand(command='start', description='Запустить бота'),
        types.BotCommand(command='help', description='Помощь'),
        types.BotCommand(command='brands', description='Смотреть бренды')
    ]
    await bot.set_my_commands(commands)
