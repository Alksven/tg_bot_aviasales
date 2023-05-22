import calendar
from states.ticket_info import FlightInfo
from datetime import date
from loder import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from utils.get_tickets.get_tickets import start_search_ticket


def split_list(iterable: list, chunk_size: int):
    """Функция для разделения инлайн кнопок"""
    return [
        iterable[index:index + chunk_size]
        for index in range(0, len(iterable), chunk_size)
    ]


def start_get_date():
    """Функция создает две инлайн кнопки для выбора текущего и следующего года"""
    current_year = date.today().year

    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text=str(current_year), callback_data=f'year:{current_year}'),
                types.InlineKeyboardButton(text=str(current_year + 1), callback_data=f'year:{current_year + 1}'),
            ],
        ],
    )


MONTH_KB = types.InlineKeyboardMarkup(
    inline_keyboard=split_list([
        types.InlineKeyboardButton(text=month, callback_data=f'month:{index}')
        for index, month in enumerate(calendar.month_name) if month
    ], 3),
)
"""инлайн клавиатура для выбора месяца"""


async def date_choice(
        call: types.CallbackQuery,
        state: FSMContext,
        keyboard: types.InlineKeyboardMarkup,
):
    """
    Функция которая принимает обновляет данные состояния, редактирует сообщение и высылает следующую клавиатуру для выбора,
    Если дата или месяц однозначные добавляет "0" это нужно для api для поимка билетов

    """
    await call.message.edit_text(
        'Выберите дату',
        reply_markup=keyboard,
    )

    selected_value = call.data.split(':')[1]
    state_name = await state.get_state()
    ready_date = await state.get_data()
    if state_name in ready_date:
        if len(selected_value) == 1:
            selected_value = '0' + selected_value
        good_date = f"{ready_date[state_name]}-{selected_value}"
    else:
        good_date = selected_value
    await state.update_data({state_name: good_date})


async def input_year(call: types.CallbackQuery, state: FSMContext):
    """callback handler Который принимает Год"""
    await date_choice(call, state, MONTH_KB)


async def input_month(call: types.CallbackQuery, state: FSMContext):
    """callback handler Который принимает Месяц"""
    month = int(call.data.split(':')[1])
    state_data = await state.get_data()
    state_name = await state.get_state()

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=split_list(
            [
                types.InlineKeyboardButton(text=day, callback_data=f'day:{day}')
                for day in range(1, calendar.monthrange(int(state_data[state_name]), month)[1])
            ], 7),
        row_width=7,
    )
    await date_choice(call, state, keyboard)


async def input_day(call: types.CallbackQuery, state: FSMContext):
    """callback handler Который принимает День"""
    day = call.data.split(':')[1]
    state_name = await state.get_state()
    edit_date = await state.get_data()
    if len(day) == 1:
        day = '0' + day
    ready_date = f"{edit_date[state_name]}-{day}"
    await state.update_data({state_name: ready_date})

    if 'FlightInfo:to_date' in edit_date and len(edit_date['FlightInfo:to_date']) == 7: # если 7 значит после предыдщего шага дата готова
        await start_search_ticket(call.message, state)
    else:
        await state.set_state(FlightInfo.to_date)
        await call.message.edit_text(
            text=f"Вы выбрали {ready_date}",
            reply_markup=start_get_date(),
        )


dp.register_callback_query_handler(input_year, Text(startswith='year:'), state=FlightInfo.from_date)
dp.register_callback_query_handler(input_month, Text(startswith='month:'), state=FlightInfo.from_date)
dp.register_callback_query_handler(input_day, Text(startswith='day:'), state=FlightInfo.from_date)
dp.register_callback_query_handler(input_year, Text(startswith='year:'), state=FlightInfo.to_date)
dp.register_callback_query_handler(input_month, Text(startswith='month:'), state=FlightInfo.to_date)
dp.register_callback_query_handler(input_day, Text(startswith='day:'), state=FlightInfo.to_date)

