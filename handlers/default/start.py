from aiogram import types
from loder import dp


async def bot_start(message: types.Message):
    await message.answer(f'Привет (Name). Я бот для удобного поиска дешевых авиабилетов.')


dp.register_message_handler(bot_start, commands=["start"])