from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

import calendar
from states.ticket_info import FlightInfo
from datetime import date
from loder import dp, logger
from utils.get_tickets.get_tickets import start_search_ticket
from datetime import datetime



def split_list(iterable: list, chunk_size: int) -> list:
    """
    Разбивает список кнопок на подсписки указанного размера.

    Параметры:
    - iterable: list - исходный список.
    - chunk_size: int - размер подсписков.

    Возвращаемое значение:
    list - список из подсписков указанного размера.

    """
    return [
        iterable[index:index + chunk_size]
        for index in range(0, len(iterable), chunk_size)
    ]


def start_get_date() -> types.InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру для выбора года.

    Возвращаемое значение:
    types.InlineKeyboardMarkup - инлайн-клавиатура для выбора года.

    """
    current_year = date.today().year

    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text=str(current_year), callback_data=f'year:{current_year}'),
                types.InlineKeyboardButton(text=str(current_year + 1), callback_data=f'year:{current_year + 1}'),
            ],
        ],
    )


months = [
    'Январь',
    'Февраль',
    'Март',
    'Апрель',
    'Май',
    'Июнь',
    'Июль',
    'Август',
    'Сентябрь',
    'Октябрь',
    'Ноябрь',
    'Декабрь'
]
MONTH_KB = types.InlineKeyboardMarkup(
    inline_keyboard=split_list([
        types.InlineKeyboardButton(text=month, callback_data=f'month:{index + 1}')
        for index, month in enumerate(months) if month
    ], 3),
)
"""инлайн клавиатура для выбора месяца"""


async def date_choice(
        call: types.CallbackQuery,
        state: FSMContext,
        keyboard: types.InlineKeyboardMarkup,
):
    """
    Обрабатывает выбор даты из инлайн-клавиатуры.

    Параметры:
    - call: types.CallbackQuery - callback запрос.
    - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.
    - keyboard: types.InlineKeyboardMarkup - инлайн-клавиатура с выбором даты.

    Возвращаемое значение:
    None

    """
    await call.message.edit_text(text='Выберите дату', reply_markup=keyboard)

    selected_value: str = call.data.split(':')[1]
    state_name: str = await state.get_state()
    ready_date: dict = await state.get_data()
    if state_name in ready_date:
        good_date: str = f"{ready_date[state_name]}{selected_value.zfill(2)}"
    else:
        good_date: str = selected_value
    await state.update_data({state_name: good_date})


async def input_year(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает выбор года из инлайн-клавиатуры.

    Параметры:
    - call: types.CallbackQuery - callback запрос.
    - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.

    Возвращаемое значение:
    None

    """
    await date_choice(call, state, MONTH_KB)


async def input_month(call: types.CallbackQuery, state: FSMContext) -> None:
    """
      Обрабатывает выбор месяца из инлайн-клавиатуры.

      Параметры:
      - call: types.CallbackQuery - callback запрос.
      - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.

      Возвращаемое значение:
      None

      """
    month: int = int(call.data.split(':')[1])
    state_data: dict = await state.get_data()
    state_name: str = await state.get_state()
    keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(
        inline_keyboard=split_list(
            [
                types.InlineKeyboardButton(text=day, callback_data=f'day:{day}')
                for day in range(1, calendar.monthrange(int(state_data[state_name]), month)[1] + 1)
            ], 7),
        row_width=7,
    )
    await date_choice(call, state, keyboard)


async def input_day(call: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает выбор дня из инлайн-клавиатуры.

    Параметры:
    - call: types.CallbackQuery - callback запрос.
    - state: FSMContext - состояние FSM (Finite State Machine) для управления состояниями бота.

    Возвращаемое значение:
    None

    """
    today = datetime.now().date()
    day = call.data.split(':')[1]
    state_name = await state.get_state()
    edit_date = await state.get_data()

    yyyy, mm, dd = edit_date[state_name][:4], edit_date[state_name][4:], day.zfill(2)
    ready_date = f"{yyyy}-{mm}-{dd}"
    target_date = datetime.strptime(ready_date, "%Y-%m-%d").date()

    if target_date < today:
        logger.warning("Введена некорректная дата (Выбранная дата меньше сегодняшней)")
        ready_date = ''
        await state.update_data({state_name: ready_date})
        await call.message.edit_text(text="Вы ввели некорректную дату")
        await call.message.answer(text="Попробуйте снова.", reply_markup=start_get_date())

    else:
        await state.update_data({state_name: ready_date})
        if 'FlightInfo:to_date' in edit_date and len(edit_date['FlightInfo:to_date']) == 6: # если 7 значит после предыдщего шага дата готова
            from_date = datetime.strptime(edit_date['FlightInfo:from_date'], "%Y-%m-%d").date()
            if target_date < from_date:
                logger.warning("Введена некорректная дата (2я дата меньше 1й)")
                ready_date = ''
                await state.update_data({state_name: ready_date})
                await call.message.edit_text(text="Вы ввели некорректную дату. Попробуйте снова.",
                                             reply_markup=start_get_date())
            else:
                await start_search_ticket(call.message, state)
        else:
            await state.set_state(FlightInfo.to_date)
            await call.message.edit_text(text=f"Ищем билеты с {ready_date}\nПо какую дату?", reply_markup=start_get_date())


dp.register_callback_query_handler(input_year, Text(startswith='year:'), state=FlightInfo.from_date)
dp.register_callback_query_handler(input_month, Text(startswith='month:'), state=FlightInfo.from_date)
dp.register_callback_query_handler(input_day, Text(startswith='day:'), state=FlightInfo.from_date)
dp.register_callback_query_handler(input_year, Text(startswith='year:'), state=FlightInfo.to_date)
dp.register_callback_query_handler(input_month, Text(startswith='month:'), state=FlightInfo.to_date)
dp.register_callback_query_handler(input_day, Text(startswith='day:'), state=FlightInfo.to_date)

