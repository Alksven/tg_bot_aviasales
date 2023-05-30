from utils.get_info_ticket.info_ticket import print_info_ticket
from config_data import config
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.ticket_info import FlightInfo


async def start_search_ticket(message: types.Message, state: FSMContext) -> None:
    """
    Начинает поиск билетов и выводит информацию о первом найденном билете.

    Параметры:
    - message: types.Message - сообщение, инициировавшее команду.
    - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.

    Возвращаемое значение:
    None

    Взаимодействие с состояниями:
    - Завершает текущее состояние.
    - Устанавливает состояние FSM в FlightInfo.get_ticket.
    - Обновляет данные состояния, добавляя список найденных билетов и номер первого билета.
    - Вызывает функцию print_info_ticket для вывода информации о первом найденном билете.
    """
    user_data: dict = await state.get_data()
    await state.finish()
    list_tickets: dict = get_tickets(user_data)
    await state.set_state(FlightInfo.get_ticket)
    await state.update_data(list_tickets=list_tickets, num_ticket=1)
    await print_info_ticket(message, state)


def get_tickets(data: dict[str, str]) -> dict[int, dict[str, str]]:
    """
    Получает список билетов на основе переданных данных.

    Параметры:
    - data: Dict[str, str] - словарь с данными, содержащими информацию о городах, датах и других параметрах для поиска билетов.

    Возвращаемое значение:
    Dict[int, Dict[str, str]] - словарь с информацией о найденных билетах, где ключами являются номера билетов,
                                а значениями - словари с информацией о каждом билете.

    Исключения:
    - Может возникнуть исключение при отправке запроса или при обработке JSON-ответа.

    Примечания:
    - Формат данных в словаре должен соответствовать требованиям API для поиска билетов.
    - В данной реализации используется только первая страница с билетами (page=1) и ограничение на количество билетов (limit=15).
    """

    request_url: str = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates?"
    token_av: str = config.TOKEN_AV
    list_tickets = dict()
    params: dict = {
        "origin": data['from_city'],
        "destination": data['to_city'],
        "beginning_of_period": data['FlightInfo:from_date'],
        "period_type": data['FlightInfo:to_date'],
        "one_way": "true",
        "sorting": "price",
        "show_to_affiliates": "true",
        "page": "1",
        "limit": "15",
        "token": token_av
    }

    response: requests.get = requests.get(request_url, params=params)
    data: response.json = response.json()
    tickets: list = data["data"]
    for i_ticket, ticket in enumerate(tickets):
        list_tickets[i_ticket + 1] = ticket

    return list_tickets
