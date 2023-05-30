from aiogram import types
from loder import dp, logger
from aiogram.dispatcher import FSMContext
from states.ticket_info import FlightInfo


async def high(message: types.Message, state: FSMContext) -> None:
    """
       Отправляет пользователю информацию о самом дорогом билете.

       Параметры:
       - message: types.Message - сообщение пользователя.
       - state: FSMContext - состояние FSM (Finite State Machine) для управления диалогом с пользователем.

       Возвращаемое значение:
       None

       Исключения:
       Отсутствуют.

       """
    state_now: str = await state.get_state()

    if state_now is None:
        logger.warning("Запрос без поиска")
        await message.answer(text="Вы еще не начали поиск билетов.\nВоспользуйтесь командой /search ")
    elif state_now != "FlightInfo:get_ticket":
        await message.answer(text="Вы еще не закончили ввод данных.")
        logger.warning("Вводу команды во время работы другой команды")
        await message.delete()
    else:

        high_date: dict = await state.get_data()
        index: int = len(high_date['list_tickets'])
        origin: str = high_date['list_tickets'][index]['origin']
        flight_number: str = high_date['list_tickets'][index]['flight_number']
        date: str = high_date['list_tickets'][index]['departure_at'].split("T")[0]
        time: str = high_date['list_tickets'][index]['departure_at'].split("T")[1][:5]
        departure_at: str = f"{date} {time}"
        destination: str = high_date['list_tickets'][index]['destination']
        destination_airport: str = high_date['list_tickets'][index]['destination_airport']
        price: str = high_date['list_tickets'][index]['price']
        transfers: str = high_date['list_tickets'][index]['transfers']
        link: str = f"https://www.aviasales.ru{high_date['list_tickets'][index]['link']}"

        kb_link: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        link_but: types.InlineKeyboardButton = types.InlineKeyboardButton(text='Cсылка на рейс', url=link)
        kb_link.add(link_but)

        result: str = f"Вылетаем из: {origin} Рейс: {flight_number}\n" \
                      f"Дата: {departure_at}\n" \
                      f"Летим в: {destination} Аэропорт {destination_airport}\n" \
                      f"Цена: {price} руб.\n" \
                      f"Пересадки: {transfers}"
        await message.answer(text=result, reply_markup=kb_link)


dp.register_message_handler(high, commands=['high'], state=FlightInfo.get_ticket)
dp.register_message_handler(high, commands=['high'], state="*")
