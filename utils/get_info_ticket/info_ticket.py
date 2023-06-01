from aiogram import types
from keyboards.inline import back_forward
from aiogram.dispatcher import FSMContext
from states.ticket_info import FlightInfo
from loder import dp
from data_base.history import add_history
from aiogram.dispatcher.filters import Text
from typing import Tuple


async def get_ready_message(state: FSMContext) -> Tuple[str, str]:
    """
       Генерирует текст сообщения и ссылку на выбранный билет.

       Параметры:
       - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.

       Возвращаемое значение:
       Tuple[str, str] - кортеж, содержащий текст сообщения с информацией о выбранном билете и ссылку на билет.
       """
    data: dict = await state.get_data()
    index: int = data["num_ticket"]
    origin: str = data['list_tickets'][index]['origin']
    flight_number: str = data['list_tickets'][index]['flight_number']
    date: str = data['list_tickets'][index]['departure_at'].split("T")[0]
    time: str = data['list_tickets'][index]['departure_at'].split("T")[1][:5]
    departure_at: str = f"{date} {time}"
    destination: str = data['list_tickets'][index]['destination']
    destination_airport: str = data['list_tickets'][index]['destination_airport']
    price: str = data['list_tickets'][index]['price']
    transfers: str = data['list_tickets'][index]['transfers']
    link: str = f"https://www.aviasales.ru{data['list_tickets'][index]['link']}"

    result: str = f"Вылетаем из: {origin} Рейс: {flight_number}\n" \
                  f"Дата: {departure_at}\n" \
                  f"Летим в: {destination} Аэропорт {destination_airport}\n" \
                  f"Цена: {price} руб.\n" \
                  f"Пересадки: {transfers}\n" \
                  f"Билет {index} из {len(data['list_tickets'])}"

    text_all_tickets = "В выбранные вами даты выгодных билетов не оказалось.\nПосмотрите другие варианты:\n\n"
    if 'all_ticket' in data['list_tickets']:
        result = text_all_tickets + result
    return result, link


async def print_info_ticket(message: types.Message,  state: FSMContext) -> None:
    """
     Выводит информацию о выбранном билете.
     Добавляет кнопки "Получить ссылку на рейс" 'Предыдущий билет' 'Следующий билет'.

     Параметры:
     - message: types.Message - сообщение, для которого нужно отобразить информацию о билете.
     - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.

     Возвращаемое значение:
     None
     """
    kb_link: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
    link: types.InlineKeyboardButton = types.InlineKeyboardButton(text='Получить ссылку на рейс', callback_data="get_link")
    b_w: list = back_forward.buttons_forward_back()
    kb_link.add(link)
    kb_link.add(*b_w)
    ready_text, ready_link = await get_ready_message(state)
    await message.edit_text(text=ready_text, reply_markup=kb_link)


async def send_link(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Отправляет ссылку на выбранный рейс и обновляет сообщение с информацией о билете.

    Параметры:
    - call: types.CallbackQuery - callback запрос.
    - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.

    Возвращаемое значение:
    None
    """

    ready_text, ready_link = await get_ready_message(state)
    text: str = f'[<< Ссылка на рейс >>]({ready_link})'

    kb_link: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
    link_button: types.InlineKeyboardButton = types.InlineKeyboardButton(text='Получить ссылку на рейс', callback_data="get_link")
    b_w: list = back_forward.buttons_forward_back()
    kb_link.add(link_button)
    kb_link.add(*b_w)

    await call.message.edit_text(text=f"{ready_text}\n{text}", reply_markup=kb_link, disable_web_page_preview=True,
                                 parse_mode=types.ParseMode.MARKDOWN)
    await add_history(call, state)


dp.register_callback_query_handler(send_link, Text(startswith="get_link"), state=FlightInfo.get_ticket)