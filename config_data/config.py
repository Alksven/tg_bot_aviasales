import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

TOKEN_TG = os.getenv('TOKEN_TG')
TOKEN_AV = os.getenv('TOKEN_AV')
DEFAULT_COMMANDS = (
    ("start",  "Запустить бота ✈"),
    ("search", "Начать поиск 🔎"),
    ("low", "Показать самый дешевый билет 🛬"),
    ("high", "Показать самый дорогой билет 🛫"),
    ("history", "История просмотра 📝"),
    ("help",  "Если вы что то забыли 🆘")
)