from aiogram import types
from aiogram.dispatcher import FSMContext

from loder import dp, logger


async def bot_start(message: types.Message, state: FSMContext) -> None:
    """
    Функция-обработчик команды /start. Отправляет приветственное сообщение пользователю.

    Параметры:
    - message: types.Message - сообщение пользователя.

    Возвращаемое значение:
    None

    Исключения:
    Отсутствуют.

    """
    state_now: str = await state.get_state()
    if state_now is not None:
        logger.warning(f"Выбор команды не в завершенном состоянии: {state_now}")
        await state.reset_state()

    name_user: str = message.from_user.first_name
    await message.answer(f'Привет {name_user}. Я бот для удобного поиска дешевых авиабилетов.')


dp.register_message_handler(bot_start, commands=["start"], state="*")