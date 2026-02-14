from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💸 Затраты")],
            [KeyboardButton(text="🔁 Привычки")],
            [KeyboardButton(text="🛒 Шоппинг")],
            [KeyboardButton(text="📝 Заметки")],
        ],
        resize_keyboard=True,
    )
