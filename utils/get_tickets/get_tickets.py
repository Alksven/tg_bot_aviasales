import json
from utils.get_info_ticket.info_ticket import print_info_ticket
from keyboards.inline import back_forward
from config_data import config
import requests
from aiogram import types
from loder import dp, bot
from aiogram.dispatcher import FSMContext
from states.ticket_info import FlightInfo


async def start_search_ticket(message: types.Message, state: FSMContext):
    """Функция завершает сбор данных"""
    user_data = await state.get_data()
    await state.finish()
    list_tickets = get_tickets(user_data)
    await state.set_state(FlightInfo.get_ticket)
    await state.update_data(list_tickets=list_tickets, num_ticket=1)
    await print_info_ticket(message, state)
    # await message.answer(text=f'{info}', reply_markup=back_forward.ticket_selection())



def get_tickets(data):
    """В этой функции получаем список билетов"""
    request_url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates?"
    token_av = config.TOKEN_AV
    list_tickets = dict()
    params = {
        "origin": data['from_city'],
        "destination": data['to_city'],
        "beginning_of_period": data['FlightInfo:from_date'],
        "period_type": data['FlightInfo:to_date'],
        "one_way": "true",
        "sorting": "price",
        "show_to_affiliates": "true",
        "page": "1",
        "limit": "10",
        "token": token_av
    }

    response = requests.get(request_url, params=params)
    data = response.json()
    tickets = data["data"]
    for i_ticket, ticket in enumerate(tickets):
        list_tickets[i_ticket + 1] = ticket

    return list_tickets
