from aiogram.dispatcher.filters.state import State, StatesGroup


class HistoryInfo(StatesGroup):
    get_list_history = State()