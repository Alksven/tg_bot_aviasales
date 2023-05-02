from aiogram.dispatcher import FSMContext
from aiogram import Bot, executor, Dispatcher, types
from states.ticket_info import FlightInfo
from main import dp

# @dp.message_handler(commands=['hello_world'])
# async def hello_world(message: types.Message, state: FSMContext):
#
#     await message.answer('Начнем поиск')
#     await state.set_state(FlightInfo.from_city)
#     await message.answer('Из какого города вылетаем?')
#
#
# @dp.message_handler(state=FlightInfo.from_city)
# async def get_city_from(message: types.Message, state: FSMContext):
#     await state.update_data(from_city=message.text)
#     await state.set_state(FlightInfo.to_city)
#     await message.answer('Куда летим?')
#
#
# @dp.message_handler(state=FlightInfo.to_city)
# async def get_city_to(message: types.Message, state: FSMContext):
#     await state.update_data(to_city=message.text)
#     await state.set_state(FlightInfo.from_date)
#     await message.answer('С какого числа ищем билеты?')
#
#
# @dp.message_handler(state=FlightInfo.from_date)
# async def get_date_from(message: types.Message, state: FSMContext):
#     await state.update_data(from_date=message.text)
#     await state.set_state(FlightInfo.to_date)
#     await message.answer('По какое число ищем билеты?')
#
#
# @dp.message_handler(state=FlightInfo.to_date)
# async def get_date_to(message: types.Message, state: FSMContext):
#     await state.update_data(to_date=message.text)
#     user_data = await state.get_data()
#     await state.finish()
#     await message.answer('Закончили')
