import json
from config_data import config
import requests


def get_tickets(data):
    """В этой функции получаем список билетов"""
    token_av = config.TOKEN_AV
    origin = data['from_city']
    destination = data['to_city']
    departure_at = ''
    return_at = ''
    start_ticket = 'https://www.aviasales.ru'
    url = requests.get(f'https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin={origin}&destination={destination}&currency=&departure_at={departure_at}&return_at={return_at}&sorting=price&direct=true&limit=10&token={token_av}')
    data = json.loads(url.text)

    info_ticket = f"Вылетаем {origin}\nЛетим в {destination}\nДата {data['data'][0]['departure_at']}\nЦена {data['data'][0]['price']}"
    return info_ticket


# a = {'from_city': "LED", 'to_city': "OMS" }
#
# get_tickets(a)

"""
currency — валюта цен на билеты. Значение по умолчанию — rub.
origin — пункт отправления. IATA-код города или аэропорта. Длина не менее двух и не более трёх символов. Необходимо указать, если нет destination.
destination — пункт назначения. IATA-код города или аэропорта. Длина не менее двух и не более трёх. Необходимо указать, если нет origin.
departure_at (необязательно)— дата вылета из пункта отправления (в формате YYYY-MM или YYYY-MM-DD).
return_at (необязательно) — дата возвращения. Чтобы получить билеты в один конец, оставьте это поле пустым.
one_way (необязательно) — билет в одну сторону. Принимает значения true илиfalse. По умолчаниюtrue. При значении true возвращает 1 билет. Используйте значение false, чтобы получить больше предложений.
direct — получить рейсы без пересадок. Принимает значения true или false. По умолчанию false.
market — задаёт маркет источника данных (по умолчанию ru).
limit — количество записей в ответе. Значение по умолчанию — 30. Не более 1000.
page — номер страницы. Используется, чтобы пропустить первые записи. То есть, выдача будет отдавать билеты в диапазоне [(page — 1) * limit; page * limit]. Таким образом, если мы хотим получить билеты с 100 по 150, то мы должны установить page=3, а limit=50.
sorting — сортировка цен:
price — по цене (значение по умолчанию).
route — по популярности маршрута.
unique — возвращает только уникальные направления, если был указан origin, но не указан destination. Позволяет собрать топ самых дешевых билетов из указанного города. Принимает значения true или false. По умолчанию false.
"""