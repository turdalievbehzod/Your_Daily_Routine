from aiogram.fsm.state import State, StatesGroup


class HabitStates(StatesGroup):
    name = State()
    month = State()
    day = State()
    hour = State()
    edit_name = State()
    edit_month = State()
    edit_day = State()
    edit_hour = State()
