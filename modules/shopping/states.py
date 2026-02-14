from aiogram.fsm.state import State, StatesGroup


class ShoppingStates(StatesGroup):
    add_item = State()
    delete_item = State()
