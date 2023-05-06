from aiogram import types
from loder import dp, bot
from utils.code_city.iata_code import get_code_city
from utils.get_tickets.get_tickets import get_tickets
from aiogram.dispatcher import FSMContext
from states.ticket_info import FlightInfo
from keyboards.reply.calendar import start_date
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP


@dp.message_handler(commands=['search'])
async def search(message: types.Message, state: FSMContext):
    await message.answer('Начнем поиск')
    await state.set_state(FlightInfo.from_city)
    await message.answer('Откуда?')


@dp.message_handler(state=FlightInfo.from_city)
async def get_city_from(message: types.Message, state: FSMContext):
    code = get_code_city(message.text)
    await state.update_data(from_city=code)
    await state.set_state(FlightInfo.to_city)
    await message.answer('Куда?')


@dp.message_handler(state=FlightInfo.to_city)
async def get_city_to(message: types.Message, state: FSMContext):
    code = get_code_city(message.text)
    await state.update_data(to_city=code)
    await state.set_state(FlightInfo.from_date)
    await message.answer('С какого числа ищем билеты?')
    date = await start_date(message.chat.id)
    await message.answer(date)

@dp.message_handler(state=FlightInfo.from_date)
async def get_date_from(message: types.Message, state: FSMContext):
    await state.update_data(from_date=0)
    print(get_date_to.date)
    await state.set_state(FlightInfo.to_date)
    await message.answer('По какое число ищем билеты?')


@dp.message_handler(state=FlightInfo.to_date)
async def get_date_to(message: types.Message, state: FSMContext):
    await state.update_data(to_date=message.text)
    user_data = await state.get_data()
    print(user_data)
    await state.finish()
    result = get_tickets(user_data)
    await message.answer(result)
