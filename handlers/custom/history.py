from aiogram import types
from loder import dp, bot
from utils.get_info_ticket.info_ticket import print_info_ticket
from utils.get_tickets.get_tickets import get_tickets
from aiogram.dispatcher import FSMContext
from states.history_state import HistoryInfo
from data_base.history import get_history
from keyboards.inline import add_date
from utils.code_city.iata_code import get_code_city


async def history(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    data = get_history(user_id)
    await state.set_state(HistoryInfo.get_list_history)
    await bot.send_message(chat_id=user_id, text='Ваша история просмотра')
    for ticket in data:
        origin = ticket[0]
        destination = ticket[1]
        departure_at = ticket[2]
        price = ticket[3]
        link =  ticket[4]
        text = f"{origin} --> {destination}\n{departure_at}\n{price} руб.\n['Ссылка на рейс']({link})"
        await bot.send_message(chat_id=user_id,  text=text, disable_web_page_preview=True, parse_mode=types.ParseMode.MARKDOWN)
        await state.finish()



dp.register_message_handler(history, commands=['history'])
