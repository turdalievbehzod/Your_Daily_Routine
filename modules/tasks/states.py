from aiogram.fsm.state import State, StatesGroup


class NoteStates(StatesGroup):
    add_mode = State()
    new_category = State()
    choose_existing_category = State()
    note_body = State()
    delete_note = State()
