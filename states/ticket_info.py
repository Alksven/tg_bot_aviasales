from aiogram.dispatcher.filters.state import State, StatesGroup


class FlightInfo(StatesGroup):
    from_city = State()
    to_city = State()
    from_date = State()
    to_date = State()

