from __future__ import annotations

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from modules.habits.services import add_habit, delete_habit, get_habit, list_habits, update_habit
from modules.habits.states import HabitStates

router = Router()
PAGE_SIZE = 6


def habits_root_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить привычку", callback_data="habits:add")],
            [InlineKeyboardButton(text="🗑 Удалить привычку", callback_data="habits:delete:list:1")],
            [InlineKeyboardButton(text="✏️ Редактировать привычку", callback_data="habits:edit:list:1")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main")],
        ]
    )


def _render_habits(rows: list[tuple]) -> str:
    if not rows:
        return "Нет никаких привычек."
    return "\n".join([f"• {name} — {month:02d}.{day:02d} в {hour:02d}:00" for _, name, month, day, hour in rows])


def habits_list_keyboard(rows: list[tuple], action: str, page: int) -> InlineKeyboardMarkup:
    total_pages = max(1, (len(rows) + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(1, min(page, total_pages))
    start = (page - 1) * PAGE_SIZE
    chunk = rows[start:start + PAGE_SIZE]

    keyboard = [[InlineKeyboardButton(text=row[1], callback_data=f"habits:{action}:pick:{row[0]}")] for row in chunk]

    nav_row: list[InlineKeyboardButton] = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"habits:{action}:list:{page - 1}"))
    nav_row.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="habits:noop"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"habits:{action}:list:{page + 1}"))
    keyboard.append(nav_row)
    keyboard.append([InlineKeyboardButton(text="↩️ К привычкам", callback_data="habits:open")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.callback_query(F.data == "habits:noop")
async def noop(callback: types.CallbackQuery) -> None:
    await callback.answer()


@router.message(F.text == "🔁 Привычки")
@router.callback_query(F.data == "habits:open")
async def habits_open(event: types.Message | types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    rows = list_habits(event.from_user.id)
    text = "🔁 Ваши привычки:\n\n" + _render_habits(rows)
    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text, reply_markup=habits_root_keyboard())
        await event.answer()
    else:
        await event.answer(text, reply_markup=habits_root_keyboard())


@router.callback_query(F.data == "habits:add")
async def habits_add_start(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Введите название привычки:")
    await state.set_state(HabitStates.name)
    await callback.answer()


@router.message(HabitStates.name)
async def habits_add_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text.strip())
    await message.answer("Введите месяц напоминания (1-12):")
    await state.set_state(HabitStates.month)


@router.message(HabitStates.month)
async def habits_add_month(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit() or not (1 <= int(message.text) <= 12):
        await message.answer("Месяц должен быть числом от 1 до 12.")
        return
    await state.update_data(month=int(message.text))
    await message.answer("Введите день месяца (1-31):")
    await state.set_state(HabitStates.day)


@router.message(HabitStates.day)
async def habits_add_day(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit() or not (1 <= int(message.text) <= 31):
        await message.answer("День должен быть числом от 1 до 31.")
        return
    await state.update_data(day=int(message.text))
    await message.answer("Введите час напоминания (0-23):")
    await state.set_state(HabitStates.hour)


@router.message(HabitStates.hour)
async def habits_add_hour(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit() or not (0 <= int(message.text) <= 23):
        await message.answer("Час должен быть числом от 0 до 23.")
        return

    data = await state.get_data()
    add_habit(message.from_user.id, data["name"], data["month"], data["day"], int(message.text))
    await state.clear()
    await message.answer(
        "✅ Привычка добавлена.\n⚠️ Бот будет тревожить вас сообщением в указанное время.",
        reply_markup=habits_root_keyboard(),
    )


@router.callback_query(F.data.startswith("habits:delete:list:"))
@router.callback_query(F.data.startswith("habits:edit:list:"))
async def habits_pick_list(callback: types.CallbackQuery) -> None:
    _, action, _, page = callback.data.split(":")
    rows = list_habits(callback.from_user.id)
    if not rows:
        await callback.answer("Привычек нет.")
        return
    page_num = int(page)
    await callback.message.edit_text(
        "Выберите привычку:",
        reply_markup=habits_list_keyboard(rows, action, page_num),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("habits:delete:pick:"))
async def habits_delete(callback: types.CallbackQuery) -> None:
    habit_id = int(callback.data.split(":")[-1])
    ok = delete_habit(callback.from_user.id, habit_id)
    await callback.message.edit_text(
        "✅ Привычка удалена." if ok else "Не удалось удалить привычку.",
        reply_markup=habits_root_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("habits:edit:pick:"))
async def habits_edit_pick(callback: types.CallbackQuery, state: FSMContext) -> None:
    habit_id = int(callback.data.split(":")[-1])
    habit = get_habit(callback.from_user.id, habit_id)
    if not habit:
        await callback.answer("Привычка не найдена.")
        return

    await state.update_data(edit_habit_id=habit_id)
    await callback.message.answer("Введите новое название привычки:")
    await state.set_state(HabitStates.edit_name)
    await callback.answer()


@router.message(HabitStates.edit_name)
async def edit_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text.strip())
    await message.answer("Новый месяц (1-12):")
    await state.set_state(HabitStates.edit_month)


@router.message(HabitStates.edit_month)
async def edit_month(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit() or not (1 <= int(message.text) <= 12):
        await message.answer("Месяц должен быть 1-12.")
        return
    await state.update_data(month=int(message.text))
    await message.answer("Новый день (1-31):")
    await state.set_state(HabitStates.edit_day)


@router.message(HabitStates.edit_day)
async def edit_day(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit() or not (1 <= int(message.text) <= 31):
        await message.answer("День должен быть 1-31.")
        return
    await state.update_data(day=int(message.text))
    await message.answer("Новый час (0-23):")
    await state.set_state(HabitStates.edit_hour)


@router.message(HabitStates.edit_hour)
async def edit_hour(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit() or not (0 <= int(message.text) <= 23):
        await message.answer("Час должен быть 0-23.")
        return

    data = await state.get_data()
    update_habit(
        user_id=message.from_user.id,
        habit_id=data["edit_habit_id"],
        name=data["name"],
        month=data["month"],
        day=data["day"],
        hour=int(message.text),
    )
    await state.clear()
    await message.answer("✅ Привычка обновлена.", reply_markup=habits_root_keyboard())
