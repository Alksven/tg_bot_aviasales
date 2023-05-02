from aiogram import Bot, executor, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv, find_dotenv
from aiogram.dispatcher import FSMContext
from states.ticket_info import FlightInfo
from code_city import get_code_city
from cheap_ticket import get_tickets



load_dotenv()
storage = MemoryStorage()
bot = Bot(os.getenv('TOKEN_TG'))
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def hello_world(message: types.Message):
    await message.answer('Привет я бот для удобного поиска дешевых авиабилетов.')


@dp.message_handler(commands=['help'])
async def hello_world(message: types.Message):
    await message.answer('Во мне пока две команды /start и /help')


@dp.message_handler(commands=['search'])
async def search(message: types.Message, state: FSMContext):
    """тут начинается первая команда, как перенести ее в другйо файл, пока не додумался"""
    await message.answer('Начнем поиск')
    await state.set_state(FlightInfo.from_city)
    await message.answer('Из какого города вылетаем?')


@dp.message_handler(state=FlightInfo.from_city)
async def get_city_from(message: types.Message, state: FSMContext):
    code = get_code_city(message.text)
    await state.update_data(from_city=code)
    await state.set_state(FlightInfo.to_city)
    await message.answer('Куда летим?')


@dp.message_handler(state=FlightInfo.to_city)
async def get_city_to(message: types.Message, state: FSMContext):
    code = get_code_city(message.text)
    await state.update_data(to_city=code)
    await state.set_state(FlightInfo.from_date)
    await message.answer('С какого числа ищем билеты?')


@dp.message_handler(state=FlightInfo.from_date)
async def get_date_from(message: types.Message, state: FSMContext):
    await state.update_data(from_date=message.text)
    await state.set_state(FlightInfo.to_date)
    await message.answer('По какое число ищем билеты?')


@dp.message_handler(state=FlightInfo.to_date)
async def get_date_to(message: types.Message, state: FSMContext):
    await state.update_data(to_date=message.text)
    user_data = await state.get_data()
    await state.finish()
    await message.answer('Закончили')
    await get_tickets(user_data)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
