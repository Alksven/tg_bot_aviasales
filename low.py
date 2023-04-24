import requests
import json
from config import TOKEN_AV


def get_iata_codes(cities):
    """Делает запрос к API Aviasales чтобы получить IATA (MOW, OVB) код городов"""
    url = requests.get(f'https://www.travelpayouts.com/widgets_suggest_params?q={cities}')
    data = json.loads(url.text)
    # from_city = data['origin']['iata']
    # to_city = data['destination']['iata']
    print(data)
    # return get_tiket(from_city, to_city)


# def get_tiket(iata_1, iata_2):
#     url = requests.get(f'https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin={iata_1}&token={TOKEN_AV}')
#     data = json.loads(url.text)
#     print(data)
#
#
# get_tiket('MOW', 'MOW')