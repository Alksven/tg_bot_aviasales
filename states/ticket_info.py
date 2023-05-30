from aiogram.dispatcher.filters.state import State, StatesGroup


class FlightInfo(StatesGroup):
    """
    Группа состояний для информации о полете.

    Состояния:
    - from_city: Состояние выбора города отправления.
    - to_city: Состояние выбора города прибытия.
    - from_date: Состояние выбора периода даты отправления.
    - to_date: Состояние выбора периода даты отправления.
    - get_ticket: Состояние получения билета.
    """
    from_city = State()
    to_city = State()
    from_date = State()
    to_date = State()
    get_ticket = State()