from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import date
import calendar
from aiogram.dispatcher.filters import Text
from loder import dp, bot
from aiogram.dispatcher import FSMContext




async def get_date():
    today_year = date.today().year
    next_year = today_year + 1
    ikb_year = InlineKeyboardMarkup()
    ikb_now_year = InlineKeyboardButton(text=str(today_year), callback_data=f'year_{today_year}')
    ikb_next_year = InlineKeyboardButton(text=str(next_year), callback_data=f'year_{next_year}')
    ikb_year.add(ikb_now_year, ikb_next_year)
    return ikb_year


@dp.callback_query_handler(Text(startswith='year_'), state='*')
@dp.callback_query_handler(Text(startswith='month_'), state='*')
@dp.callback_query_handler(Text(startswith='day_'), state='*')
async def process_date(callback_query: CallbackQuery, state: FSMContext):

    if callback_query.data.startswith('year_'):
        selected_year = callback_query.data.split('_')[1]
        await state.update_data(date=selected_year)

        months = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль', 8:'Август',
                  9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}
        button_list = []
        if selected_year == str(date.today().year):
            today_month = date.today().month
        else:
            today_month = 1
        for i_month in range(today_month, len(months) + 1):
            button = InlineKeyboardButton(text=months[i_month], callback_data=f'month_{i_month}')
            button_list.append(button)
        ikb_month = InlineKeyboardMarkup()
        for i in range(0, len(button_list), 3):
            ikb_month.row(*button_list[i:i+3])
        await bot.send_message(callback_query.from_user.id, f"Выберите месяц:", reply_markup=ikb_month)


    elif callback_query.data.startswith('month_'):
        user_data = await state.get_data()
        year = user_data['date']
        selected_month = callback_query.data.split('_')[1]
        # Получить количество дней в указанном месяце
        days_in_month = calendar.monthrange(int(year), int(selected_month))[1]
        if len(selected_month) == 1:
            selected_month = '0' + selected_month
            year_m = f'{year}-{selected_month}'
            await state.update_data(date=year_m)

        button_list_day = []
        for i_day in range(1, days_in_month + 1):
            button = InlineKeyboardButton(text=str(i_day), callback_data=f'day_{i_day}')
            button_list_day.append(button)
        ikb_day = InlineKeyboardMarkup()
        for i in range(0, len(button_list_day), 5):
            ikb_day.row(*button_list_day[i:i+5])
        await bot.send_message(callback_query.from_user.id, f"Выберите день:", reply_markup=ikb_day)

    elif callback_query.data.startswith('day_'):
        selected_day = callback_query.data.split('_')[1]
        if len(selected_day) == 1:
            selected_day = '0' + selected_day
        user_data = await state.get_data()
        y_m = user_data['date']
        date_ready = f'{y_m}-{selected_day}'
        await state.update_data(date=date_ready)
        await callback_query.answer(text=f'Вы выбрали дату {date_ready}')
        print(date_ready)
