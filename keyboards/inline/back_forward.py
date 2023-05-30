from loder import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.get_info_ticket import info_ticket
from loder import logger


def buttons_forward_back() -> list[types.InlineKeyboardButton]:
    """
    Создает инлайн-кнопки 'Предыдущий билет' 'Следующий билет'

    Возвращаемое значение:
    list: - инлайн-кнопки 'Предыдущий билет' 'Следующий билет'

    """
    back: types.InlineKeyboardButton = types.InlineKeyboardButton(text='Предыдущий билет', callback_data="back:step")
    forward: types.InlineKeyboardButton = types.InlineKeyboardButton(text='Следующий билет', callback_data="forward:step")
    return [back, forward]


async def step_back(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает нажатие кнопки "Предыдущий билет".

    Параметры:
    - call: types.CallbackQuery - callback запрос.
    - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.

    Возвращаемое значение:
    None
    """
    data: dict = await state.get_data()
    if data['num_ticket'] == 1:
        logger.warning(f"выходи из диапазона {data['num_ticket']}")
        await call.answer(text="Это и так первый билет")
    else:
        num_ticket: int = data['num_ticket'] + -1
        await state.update_data(num_ticket=num_ticket)
        await info_ticket.print_info_ticket(call.message, state)


async def step_forward(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает нажатие кнопки "Следующий билет".

    Параметры:
    - call: types.CallbackQuery - callback запрос.
    - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.

    Возвращаемое значение:
    None
    """
    data: dict = await state.get_data()
    if data['num_ticket'] == len(data['list_tickets']):
        logger.warning(f"выходи из диапазона {data['num_ticket']}")
        await call.answer(text="Это и так последний билет")
    else:
        num_ticket:int = data['num_ticket'] + 1
        await state.update_data(num_ticket=num_ticket)
        await info_ticket.print_info_ticket(call.message, state)


dp.register_callback_query_handler(step_back, text='back:step', state="*")
dp.register_callback_query_handler(step_forward, text="forward:step", state="*")