from aiogram import Bot, executor, Dispatcher, types

bot = Bot('6277014067:AAGmaSq-NGWyVXGqJZlOcoim28InDurhsPE')
dp = Dispatcher(bot)


@dp.message_handler(commands=['hello_world'])
async def hello_world(message: types.Message):
    await message.answer('Вы введи команду "hello-world"')


@dp.message_handler(text=['привет', 'Привет'])
async def message_world(message: types.Message):
    await message.answer('Привет, Привет')


if __name__ == "__main__":
    executor.start_polling(dp)
