import sqlite3
from aiogram.dispatcher import FSMContext
import os
from loder import logger


def start_db() -> None:
    """
      Запускает базу данных и создает необходимую таблицу, если она не существует.

      Параметры:
      None

      Возвращаемое значение:
      None

      Исключения:
      Отсутствуют.
      """
    logger.info("БД запущена")
    db_path: str = os.path.join(os.path.dirname(__file__), 'user_history.db')
    global base, cur
    base = sqlite3.connect(db_path)
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS data('
                 'user_id, '
                 'airline, '
                 'departure_at, '
                 'destination, '
                 'destination_airport, '
                 'duration, '
                 'duration_back, '
                 'duration_to, '
                 'flight_number, '
                 'link, '
                 'origin, '
                 'origin_airport, '
                 'price, '
                 'return_transfers, '
                 'transfers)')
    base.commit()


async def add_history(message, state: FSMContext) -> None:
    """
    Функция, добавляет в БД историю просмотров рейсов пользователя.

        Параметры:
        - message: types.Message - сообщение пользователя.
        - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.

       Возвращаемое значение:
        None
    """
    state_now: str = await state.get_state()
    if state_now == 'FlightInfo:get_ticket':
        data: dict = await state.get_data()
        user_id: str = message.from_user.id
        index : int = data["num_ticket"]
        data['list_tickets'][index]['user_id']: str = user_id
        data['list_tickets'][index]['link']: str = f"https://www.aviasales.ru{data['list_tickets'][index]['link']}"

        fields = ', '.join(data['list_tickets'][index].keys())
        placeholders: str = ', '.join('?' * len(data['list_tickets'][index]))
        sql_query: str = f'INSERT INTO data ({fields}) VALUES ({placeholders})'
        cur.execute(sql_query, tuple(data['list_tickets'][index].values()))
        base.commit()


def get_history(user_id) -> list:
    """
    Функция, получает историю просмотра пользователя. (до 10 записей)

    Параметры:
    - user_id: str - id пользователя

    Возвращаемое значение:
    search_history: list - список с историей запросов.
    """
    cur.execute(f'SELECT origin, destination,departure_at, price, link FROM data WHERE user_id == {user_id} LIMIT 10')

    search_history: list = cur.fetchall()
    return search_history
