import requests
import json
import pprint


def get_code_city(city):
    """чтобы найти билет нужно получить IATA-код города. Данная функция получает этот код.,
    """
    url = requests.get(f'https://autocomplete.travelpayouts.com/places2?locale=en&types[]=airport&types[]=city&term={city}')
    data = json.loads(url.text)
    return data[0]['code']
# потом еще нужно возвращать название города  'name': 'Moscow',


