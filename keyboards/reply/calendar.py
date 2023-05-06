from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from loder import dp, bot
from states.ticket_info import FlightInfo

@dp.callback_query_handler()
async def start_date(chat_id):
    calendar, step = DetailedTelegramCalendar().build()
    await bot.send_message(chat_id,
                           f"Выберите {LSTEP[step]}",
                           reply_markup=calendar)


@dp.callback_query_handler(DetailedTelegramCalendar.func(), state=FlightInfo.from_date)
async def inline_kb_answer_callback_handler(query):
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
        return result