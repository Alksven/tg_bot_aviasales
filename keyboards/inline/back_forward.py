from loder import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.get_info_ticket import info_ticket


def ticket_selection():
    """Инлайн клавиатура с двумя кнопками, 'Предыдущий билет', 'Следующий билет"""
    kb_back_forward = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton(text='Предыдущий билет', callback_data="back:step")
    forward = types.InlineKeyboardButton(text='Следующий билет', callback_data="forward:step")
    kb_back_forward.add(back, forward)
    return [back, forward]


async def step_back(call: types.CallbackQuery, state: FSMContext):
    """callback handler который обрабатывает шаг Назад"""
    date = await state.get_data()
    num_ticket = date['num_ticket'] + -1
    # Прописать проверку на последний билет
    await state.update_data(num_ticket=num_ticket)
    await info_ticket.print_info_ticket(call.message, state)


async def step_forward(call: types.CallbackQuery, state: FSMContext):
    """callback handler который обрабатывает шаг Вперед"""
    date = await state.get_data()
    num_ticket = date['num_ticket'] + 1
    #Прописать проверку на последний билет
    await state.update_data(num_ticket=num_ticket)
    await info_ticket.print_info_ticket(call.message, state)


dp.register_callback_query_handler(step_back, text='back:step', state="*")
dp.register_callback_query_handler(step_forward, text="forward:step", state="*")