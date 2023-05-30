from aiogram.dispatcher.filters.state import State, StatesGroup


class HistoryInfo(StatesGroup):
    """
    Группа состояний для информации о истории.

    Состояния:
    - get_list_history: Состояние получения списка истории.
    """
    get_list_history = State()