from aiogram import types
from keyboards.inline import back_forward
from aiogram.dispatcher import FSMContext
from states.ticket_info import FlightInfo



async def print_info_ticket(message: types.Message,  state: FSMContext):
    """Отправляем пользователю информацию о билете"""
    date = await state.get_data()
    index = date["num_ticket"]

    start_ticket = 'https://www.aviasales.ru'
    origin = date['list_tickets'][index]['origin']
    flight_number = date['list_tickets'][index]['flight_number']
    departure_at = date['list_tickets'][index]['departure_at']
    destination = date['list_tickets'][index]['destination']
    destination_airport = date['list_tickets'][index]['destination_airport']
    price = date['list_tickets'][index]['price']
    transfers = date['list_tickets'][index]['transfers']

    kb_link = types.InlineKeyboardMarkup()
    link = types.InlineKeyboardButton(text='Ссылка на билет', url=start_ticket + date['list_tickets'][index]['link'], callback_data='add_history')
    b_w = back_forward.ticket_selection()
    kb_link.add(link)
    kb_link.add(*b_w)


    result = f"Вылетаем из: {origin} Рейс: {flight_number}\n" \
             f"Дата: {departure_at}\n" \
             f"Летим в: {destination} Аэропорт {destination_airport}\n" \
             f"Цена: {price} руб.\n" \
             f"Пересадки: {transfers}\n" \
             f"Билет номер {index}"
    await message.edit_text(text=result, reply_markup=kb_link)
