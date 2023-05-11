from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from loder import dp, bot
from states.ticket_info import FlightInfo
from aiogram.dispatcher import FSMContext
from datetime import date, timedelta


# @dp.callback_query_handler()
async def start_date(chat_id):
    today = date.today()
    one_years_later = today.replace(year=today.year + 1)
    calendar, step = DetailedTelegramCalendar(min_date=today, max_date=one_years_later).build()
    await bot.send_message(chat_id,
                           f"Выберите {LSTEP[step]}",
                           reply_markup=calendar)


@dp.callback_query_handler(DetailedTelegramCalendar.func(), state=FlightInfo.from_date)
async def inline_kb_answer_callback_handler_from_date(query, state: FSMContext):
    result, key, step = DetailedTelegramCalendar().process(query.data)

    if not result and key:
        await bot.edit_message_text(f"Select {LSTEP[step]}",
                                    query.message.chat.id,
                                    query.message.message_id,
                                    reply_markup=key)
    elif result:
        await bot.edit_message_text(f"You selected {result}",
                                    query.message.chat.id,
                                    query.message.message_id)
        year = str(result.year)
        month = str(result.month)
        if len(month) == 1:
            month = '0' + month
        day = str(result.day)
        if len(day) == 1:
            day = '0' + day
        await state.update_data(from_date=f'{year}-{month}-{day}')



@dp.callback_query_handler(DetailedTelegramCalendar.func(), state=FlightInfo.to_date)
async def inline_kb_answer_callback_handler_to_date(query, state: FSMContext):
    result, key, step = DetailedTelegramCalendar().process(query.data)

    if not result and key:
        await bot.edit_message_text(f"Select {LSTEP[step]}",
                                    query.message.chat.id,
                                    query.message.message_id,
                                    reply_markup=key)
    elif result:

        year = str(result.year)
        month = str(result.month)
        if len(month) == 1:
            month = '0' + month
        day = str(result.day)
        if len(day) == 1:
            day = '0' + day
        await state.update_data(to_date=f'{year}-{month}-{day}')
        await bot.edit_message_text(f"You selected {result}",
                                    query.message.chat.id,
                                    query.message.message_id)