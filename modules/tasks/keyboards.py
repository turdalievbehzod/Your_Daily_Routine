from aiogram.types import KeyboardButton, ReplyKeyboardMarkup



def categories_keyboard(categories: list[str]) -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=title)] for title in categories]
    keyboard.append([KeyboardButton(text="❌ Отмена")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
