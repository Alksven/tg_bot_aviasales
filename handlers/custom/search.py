from aiogram import types
from loder import dp
from utils.get_tickets.get_tickets import get_tickets
from aiogram.dispatcher import FSMContext
from states.ticket_info import FlightInfo
from keyboards.inline import add_date
from utils.code_city.iata_code import get_code_city


async def search(message: types.Message, state: FSMContext):
    """
    Функция начала поиска, устанавливается состояние FlightInfo.from_city и запрашивается город вылета
    """
    await message.answer('Начнем поиск')
    await state.set_state(FlightInfo.from_city)
    await message.answer('Откуда?')


async def get_city_from(message: types.Message, state: FSMContext):
    """
    Функция записывает в состояние город вылета и устанавливается состояние FlightInfo.to_city и
    запрашивает город прибытия
    """
    code = "LED" #get_code_city(message.text)
    await state.update_data(from_city=code)
    await state.set_state(FlightInfo.to_city)
    await message.answer('Куда?')


async def get_city_to(message: types.Message, state: FSMContext):
    """
    Функция записывает в состояние город прибытия, устанавливается состояние FlightInfo.from_date и
    запрашивает с какой даты искать билеты, путем отправки инлайн клавиатуры
    """
    code = "MOW" #get_code_city(message.text)
    await state.update_data(to_city=code)
    await state.set_state(FlightInfo.from_date)
    await message.answer(text='Выберите дату', reply_markup=add_date.start_get_date())





dp.register_message_handler(search, commands=['search'])
dp.register_message_handler(get_city_from, state=FlightInfo.from_city)
dp.register_message_handler(get_city_to, state=FlightInfo.to_city)
