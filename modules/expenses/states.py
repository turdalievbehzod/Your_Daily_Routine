from aiogram.fsm.state import State, StatesGroup


class ExpenseStates(StatesGroup):
    category = State()
    amount = State()
    delete_id = State()
