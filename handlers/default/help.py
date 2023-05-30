from aiogram import types
from loder import dp, logger
from config_data import config
from aiogram.dispatcher import FSMContext


async def bot_help(message: types.Message, state: FSMContext) -> None:
    """
    Функция обработки команды '/help'.

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
    text: list = [f"/{command} - {desk}" for command, desk in config.DEFAULT_COMMANDS]
    await message.reply('\n'.join(text))


dp.register_message_handler(bot_help, commands=["help"], state="*")
