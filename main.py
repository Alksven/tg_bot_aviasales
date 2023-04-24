from aiogram import Bot, executor, Dispatcher, types
import low
from config import TOKEN_TG

bot = Bot(TOKEN_TG)
dp = Dispatcher(bot)


@dp.message_handler(commands=['hello_world'])
async def hello_world(message: types.Message):
    await message.answer('Вы введи команду "hello-world"')


@dp.message_handler(text=['привет', 'Привет'])
async def message_world(message: types.Message):
    await message.answer('Привет, Привет')

@dp.message_handler()
async def message_world(message: types.Message):
    """
    Функция запрашивать у пользователя из какого, в какой город летим
    и получает IATA код городов ( нужно для дальнейшего использования)
    Эта функция должна срабатывать после команды /low но ни как не понимаю как это сделать.
    """
    result = low.get_iata_codes(message.text)
    await message.answer(f'{result[0]} {result[1]}')


if __name__ == "__main__":
    executor.start_polling(dp)
