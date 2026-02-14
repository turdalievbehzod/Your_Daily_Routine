from __future__ import annotations

from decimal import Decimal, InvalidOperation

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from modules.expenses.keyboards import details_keyboard, expenses_actions_keyboard
from modules.expenses.services import (
    add_expense,
    delete_expense_last_month,
    get_detailed_for_period,
    get_month_expenses,
    get_total_for_all_time,
    get_total_for_current_year,
)
from modules.expenses.states import ExpenseStates

router = Router()


def _format_expenses(rows: list[tuple], with_id: bool = False) -> str:
    if not rows:
        return "Пока нет расходов за выбранный период."

    lines: list[str] = []
    for row in rows:
        if with_id:
            expense_id, category, amount, created_at = row
            lines.append(f"• ID {expense_id}: {category} — {amount}₽ ({created_at:%d.%m.%Y})")
        else:
            category, amount, created_at = row
            lines.append(f"• {category} — {amount}₽ ({created_at:%d.%m.%Y})")
    return "\n".join(lines)


@router.message(F.text == "💸 Затраты")
@router.callback_query(F.data == "expenses:open")
async def open_expenses(event: types.Message | types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    user_id = event.from_user.id
    text = "💸 Расходы за текущий месяц:\n\n" + _format_expenses(get_month_expenses(user_id), with_id=True)

    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text, reply_markup=expenses_actions_keyboard())
        await event.answer()
    else:
        await event.answer(text, reply_markup=expenses_actions_keyboard())


@router.callback_query(F.data == "expenses:add")
async def start_add_expense(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("На что были потрачены деньги?")
    await state.set_state(ExpenseStates.category)
    await callback.answer()


@router.message(ExpenseStates.category)
async def ask_amount(message: types.Message, state: FSMContext) -> None:
    await state.update_data(category=message.text.strip())
    await message.answer("Введите сумму расхода (только число):")
    await state.set_state(ExpenseStates.amount)


@router.message(ExpenseStates.amount)
async def finish_add_expense(message: types.Message, state: FSMContext) -> None:
    try:
        amount = Decimal(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
    except (InvalidOperation, ValueError):
        await message.answer("Некорректная сумма. Пример: 1200.50")
        return

    data = await state.get_data()
    add_expense(message.from_user.id, amount, data["category"])
    await state.clear()

    rows = get_month_expenses(message.from_user.id)
    await message.answer(
        "✅ Расход сохранён.\n\nТекущий месяц:\n" + _format_expenses(rows, with_id=True),
        reply_markup=expenses_actions_keyboard(),
    )


@router.callback_query(F.data == "expenses:delete")
async def ask_delete_id(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Введите ID расхода за текущий месяц для удаления:")
    await state.set_state(ExpenseStates.delete_id)
    await callback.answer()


@router.message(ExpenseStates.delete_id)
async def delete_expense_by_id(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("ID должен быть числом.")
        return

    deleted = delete_expense_last_month(message.from_user.id, int(message.text))
    await state.clear()
    await message.answer(
        "✅ Расход удалён." if deleted else "Не найден расход за этот месяц с таким ID.",
        reply_markup=expenses_actions_keyboard(),
    )


@router.callback_query(F.data == "expenses:year_total")
async def show_year_total(callback: types.CallbackQuery) -> None:
    total = get_total_for_current_year(callback.from_user.id)
    await callback.message.edit_text(
        f"📆 Сумма расходов за текущий год: {total}₽",
        reply_markup=details_keyboard("year"),
    )
    await callback.answer()


@router.callback_query(F.data == "expenses:all_total")
async def show_all_total(callback: types.CallbackQuery) -> None:
    total = get_total_for_all_time(callback.from_user.id)
    await callback.message.edit_text(
        f"♾ Сумма расходов за всё время: {total}₽",
        reply_markup=details_keyboard("all"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("expenses:details:"))
async def show_details(callback: types.CallbackQuery) -> None:
    period = callback.data.split(":")[-1]
    rows = get_detailed_for_period(callback.from_user.id, period)
    title = "📄 Детализация за год" if period == "year" else "📄 Детализация за всё время"
    await callback.message.edit_text(
        f"{title}:\n\n{_format_expenses(rows)}",
        reply_markup=expenses_actions_keyboard(),
    )
    await callback.answer()
