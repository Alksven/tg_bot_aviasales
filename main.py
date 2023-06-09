from aiogram import executor
from loder import dp, bot
from data_base.history import start_db
import handlers
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    """
    Функция, вызываемая при запуске бота, которая запускает БД.

    Параметры:
    - dp: Dispatcher - объект диспетчера Aiogram.

    Возвращаемое значение:
    Отсутствует.

    """
    start_db()


if __name__ == "__main__":
    set_default_commands(bot)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
