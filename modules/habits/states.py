from aiogram.fsm.state import StatesGroup, State


class HabitStates(StatesGroup):
    name = State()
    frequency = State()
