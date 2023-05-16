from aiogram import types, filters
from aiogram.dispatcher.filters import Text
from loder import dp, bot
from utils.code_city.iata_code import get_code_city
from utils.get_tickets.get_tickets import get_tickets
from aiogram.dispatcher import FSMContext
from states.ticket_info import FlightInfo
# from keyboards.reply.calendar import start_date
from keyboards.reply.add_date import get_date



@dp.message_handler(commands=['search'])
async def search(message: types.Message, state: FSMContext):
    await message.answer('Начнем поиск')
    await state.set_state(FlightInfo.from_city)
    await message.answer('Откуда?')



@dp.message_handler(state=FlightInfo.from_city)
async def get_city_from(message: types.Message, state: FSMContext):
    code = 'MOW' #get_code_city(message.text)
    await state.update_data(from_city=code)
    await state.set_state(FlightInfo.to_city)
    await message.answer('Куда?')


@dp.message_handler(state=FlightInfo.to_city)
async def get_city_to(message: types.Message, state: FSMContext):
    code = 'NOJ' #get_code_city(message.text)
    await state.update_data(to_city=code)
    await state.set_state(FlightInfo.from_date)
    kb = await get_date()
    await message.answer(text='С какого числа ищем билеты?', reply_markup=kb)



@dp.message_handler(state=FlightInfo.from_date)
async def get_date_from(message: types.Message, state: FSMContext):
    await state.set_state(FlightInfo.to_date)
    # kb = await get_date()
    await message.answer('По какое число ищем билеты?', reply_markup=kb)
    # await start_date(message.chat.id, cal_id=2)



@dp.message_handler(state=FlightInfo.to_date)
async def get_date_to(message: types.Message, state: FSMContext):
    await state.update_data(to_date=message.text)
    user_data = await state.get_data()
    print(user_data)
    await state.finish()
    result = get_tickets(user_data)
    await message.answer(result)
