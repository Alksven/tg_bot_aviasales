from aiogram import types
from loder import dp


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    await message.answer(f'Привет (Name). Я бот для удобного поиска дешевых авиабилетов.')