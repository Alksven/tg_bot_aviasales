import sqlite3
from aiogram import types
from loder import dp
from aiogram.dispatcher import FSMContext
from states.ticket_info import FlightInfo
from states.history_state import HistoryInfo
import pprint
import os


def start_db():
    db_path = os.path.join(os.path.dirname(__file__), 'user_history.db')
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


async def add_history(message, state: FSMContext):
    state_now = await state.get_state()
    if state_now == 'FlightInfo:get_ticket':
        data = await state.get_data()
        user_id = message.from_user.id
        index = data["num_ticket"]
        data['list_tickets'][index]['user_id'] = user_id
        data['list_tickets'][index]['link'] = f"https://www.aviasales.ru{data['list_tickets'][index]['link']}"

        fields = ', '.join(data['list_tickets'][index].keys())
        placeholders = ', '.join('?' * len(data['list_tickets'][index]))
        sql_query = f'INSERT INTO data ({fields}) VALUES ({placeholders})'
        cur.execute(sql_query, tuple(data['list_tickets'][index].values()))
        base.commit()


def get_history(user_id):
    cur.execute(f'SELECT origin, destination,departure_at, price, link FROM data WHERE user_id == {user_id} LIMIT 10')
    data = cur.fetchall()
    return data




