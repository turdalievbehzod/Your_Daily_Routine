from aiogram.fsm.state import StatesGroup, State


class TaskStates(StatesGroup):
    title = State()
    deadline = State()
