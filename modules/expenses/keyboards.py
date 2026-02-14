from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def expenses_actions_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Записать расходы", callback_data="expenses:add")],
            [InlineKeyboardButton(text="🗑 Удалить расход (последний месяц)", callback_data="expenses:delete")],
            [InlineKeyboardButton(text="📆 Сумма за год", callback_data="expenses:year_total")],
            [InlineKeyboardButton(text="♾ Сумма за всё время", callback_data="expenses:all_total")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main")],
        ]
    )


def details_keyboard(period: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📄 Показать детали", callback_data=f"expenses:details:{period}")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="expenses:open")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main")],
        ]
    )
