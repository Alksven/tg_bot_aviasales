import requests
import json


def get_code_city(city):
    """чтобы найти билет нужно получить IATA-код города. Данная функция получает этот код.,
    """
    url = requests.get(f'https://autocomplete.travelpayouts.com/places2?locale=en&types[]=airport&types[]=city&term={city}')
    print(url)
    data = json.loads(url.text)
    return data[0]['code']