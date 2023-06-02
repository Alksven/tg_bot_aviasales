from aiogram import types
from aiogram.dispatcher import FSMContext

from loder import dp, logger
from states.ticket_info import FlightInfo
from keyboards.inline import add_date
from utils.code_city.iata_code import get_code_city


async def search(message: types.Message, state: FSMContext) -> None:
    """
        Функция начала поиска авиабилетов. Устанавливает состояние FlightInfo.from_city
        и запрашивает у пользователя город вылета.

        Параметры:
        - message: types.Message - сообщение пользователя.
        - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.

        Возвращаемое значение:
        None

        Исключения:
        Отсутствуют.

        """
    await message.answer('Начнем поиск')
    await state.set_state(FlightInfo.from_city)
    await message.answer('Откуда вылетаем?')


async def get_city_from(message: types.Message, state: FSMContext) -> None:
    """
        Функция Принимающая город вылета. Устанавливает состояние FlightInfo.to_city
        и запрашивает у пользователя город прилета.

        Параметры:
        - message: types.Message - сообщение пользователя.
        - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.

        Возвращаемое значение:
        None

        Исключения:
        Отсутствуют.

        """

    code = get_code_city(message.text)
    try:
        if code:
            await state.update_data(from_city=code)
            await state.set_state(FlightInfo.to_city)
            await message.answer('Куда летим?')
        else:
            await message.answer('Возможно ошибся либо аэропорта нет в этом городе.\nПопробуй снова.')
    except Exception as es:
        logger.warning(es)


async def get_city_to(message: types.Message, state: FSMContext) -> None:
    """
        Функция Принимающая город прилета. Устанавливает состояние FlightInfo.from_date
        и запрашивает у пользователя дату вылета и отправляет клавиатуру для выбора года.

        Параметры:
        - message: types.Message - сообщение пользователя.
        - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.

        Возвращаемое значение:
        None

        Исключения:
        Отсутствуют.

        """
    code = get_code_city(message.text)
    try:
        if code:
            await state.update_data(to_city=code)
            await state.set_state(FlightInfo.from_date)
            await message.answer(text='С какой даты ищем билеты?', reply_markup=add_date.start_get_date())
        else:
            await message.answer('Возможно ошибся либо аэропорта нет в этом городе.\nПопробуй снова.')
    except Exception as es:
        logger.warning(es)


dp.register_message_handler(search, commands=['search'], state="*")
dp.register_message_handler(get_city_from, state=FlightInfo.from_city)
dp.register_message_handler(get_city_to, state=FlightInfo.to_city)