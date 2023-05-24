from aiogram import types
from keyboards.inline import back_forward
from aiogram.dispatcher import FSMContext
from states.ticket_info import FlightInfo
from loder import dp, bot
from data_base.history import add_history


async def print_info_ticket(message: types.Message,  state: FSMContext):
    """Отправляем пользователю информацию о билете"""
    data = await state.get_data()
    index = data["num_ticket"]
    origin = data['list_tickets'][index]['origin']
    flight_number = data['list_tickets'][index]['flight_number']
    departure_at = data['list_tickets'][index]['departure_at']
    destination = data['list_tickets'][index]['destination']
    destination_airport = data['list_tickets'][index]['destination_airport']
    price = data['list_tickets'][index]['price']
    transfers = data['list_tickets'][index]['transfers']

    kb_link = types.InlineKeyboardMarkup()
    link = types.InlineKeyboardButton(text='Получить ссылку на рейс', callback_data='get_link')
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


async def send_link(message: types.Message,  state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    index = data["num_ticket"]
    link = f"https://www.aviasales.ru{data['list_tickets'][index]['link']}"
    text = f'Ссылка: ["Ссылка"]({link})'
    await bot.send_message(chat_id=user_id,  text=text, disable_web_page_preview=True, parse_mode=types.ParseMode.MARKDOWN)
    await add_history(message, state)

dp.register_callback_query_handler(send_link, text='get_link', state=FlightInfo.get_ticket)
