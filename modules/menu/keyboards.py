from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Задачи")],
            [KeyboardButton(text="💸 Расходы")],
            [KeyboardButton(text="🔁 Привычки")],
            [KeyboardButton(text="🛒 Покупки")],
        ],
        resize_keyboard=True
    )
