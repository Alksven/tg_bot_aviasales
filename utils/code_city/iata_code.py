import requests
import json
from loder import logger
from typing import Any


def get_code_city(city: str) -> Any:
    """
        Получает код города или аэропорта по его названию.

        Параметры:
        - city: str - название города или аэропорта.

        Возвращаемое значение:
        Tuple[bool, str] - кортеж, содержащий флаг успешности операции (True - успех, False - ошибка)
                          и код города или аэропорта.

        Исключения:
        - В случае неправильного ввода города или аэропорта, вызывается исключение TypeError.
        - В случае возникновения других ошибок при обращении к API, исключение обрабатывается и логируется.
    """
    if city.isdigit():
        logger.warning("Не правильный ввод")
        return False
    else:
        url: requests.Response = requests.get(f'https://autocomplete.travelpayouts.com/places2?locale=en&types[]=airport&types[]=city&term={city}')
        if url.status_code == 200:
            data: json = json.loads(url.text)
            try:
                return data[0]['code']
            except Exception as bug:
                logger.warning(bug)
                return False
