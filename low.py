import requests
import json
import os
os.environ.get('TOKEN_AV')

# def get_iata_codes(cities):
#     """Делает запрос к API Aviasales чтобы получить IATA (MOW, OVB) код городов"""
#     city_list = list()
#     if len(cities.split()) == 1:
#         url = requests.get(f'https://www.travelpayouts.com/widgets_suggest_params?q={cities}в Новосибирск')
#         """Нельзя по одиночке искать кода городов, по этому добавляем последний город вручную и
#         после этого обрабатываем только одни город"""
#     else:
#         url = requests.get(f'https://www.travelpayouts.com/widgets_suggest_params?q={cities}')
#
#     data = json.loads(url.text)
#     city_list.append(data['origin']['iata'])
#     city_list.append(data['destination']['iata'])
#     return get_tiket(city_list)
#
#
# def get_tiket(cities):
#     url = requests.get(f'https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin={cities[0]}&token={TOKEN_AV}')
#     data = json.loads(url.text)
#     print(data)
