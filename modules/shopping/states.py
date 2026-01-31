from aiogram.fsm.state import StatesGroup, State


class ShoppingStates(StatesGroup):
    item = State()
