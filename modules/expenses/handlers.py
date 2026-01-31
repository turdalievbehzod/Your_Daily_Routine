from aiogram import Router, types

from modules.expenses.services import add_expense

router = Router()


@router.message(lambda m: m.text.startswith("💸"))
async def expense_handler(message: types.Message):
    try:
        _, amount, category = message.text.split()
        add_expense(message.from_user.id, float(amount), category)
        await message.answer("💰 Расход добавлен")
    except Exception:
        await message.answer("Пример: 💸 25000 еда")
