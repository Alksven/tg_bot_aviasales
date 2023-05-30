from aiogram import types
from loder import dp, bot, logger
from aiogram.dispatcher import FSMContext
from states.history_state import HistoryInfo
from data_base.history import get_history



async def history(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команду "/history" для получения истории просмотра пользователя.

    Параметры:
    - message: types.Message - сообщение пользователя.
    - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.

    Возвращаемое значение:
    None

    Исключения:
    Отсутствуют.
    """
    await state.finish()
    user_id: str = message.from_user.id
    data: list = get_history(user_id)
    if not data:
        await message.answer(text="Ваша история просмотра пуста.\nЧтобы начать поиск, воспользуйтесь командой /search")
        logger.warning("Запрос пустой истории")
    else:
        await state.set_state(HistoryInfo.get_list_history)
        await bot.send_message(chat_id=user_id, text='Ваша история просмотра')
        for ticket in data:
            origin: str = ticket[0]
            destination: str = ticket[1]
            date: str = ticket[2].split("T")[0]
            time: str = ticket[2].split("T")[1][:5]
            departure_at: str = f"{date} {time}"
            price: str = ticket[3]
            link: str = ticket[4]
            text: str = f"{origin} --> {destination}, Дата: {departure_at}\nЦена {price} руб. ['Ссылка на рейс']({link})"
            await bot.send_message(chat_id=user_id,  text=text, disable_web_page_preview=True, parse_mode=types.ParseMode.MARKDOWN)
            await state.finish()


dp.register_message_handler(history, commands=['history'], state="*")
