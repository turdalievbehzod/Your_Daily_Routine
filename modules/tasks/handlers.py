from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

from modules.menu.keyboards import main_menu
from modules.tasks.keyboards import categories_keyboard
from modules.tasks.services import add_note, create_category, delete_note, list_categories, list_notes
from modules.tasks.states import NoteStates

router = Router()


def notes_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить заметку", callback_data="notes:add")],
            [InlineKeyboardButton(text="🗑 Удалить заметку", callback_data="notes:delete")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main")],
        ]
    )


def add_mode_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📁 Добавить в существующую категорию", callback_data="notes:add:existing")],
            [InlineKeyboardButton(text="🆕 Добавить в новую категорию", callback_data="notes:add:new")],
            [InlineKeyboardButton(text="❌ Отменить действие", callback_data="notes:cancel")],
        ]
    )


def _render_notes(rows: list[tuple]) -> str:
    if not rows:
        return "Пока нет заметок."
    return "\n".join([f"• ID {note_id} [{category}] {body}" for note_id, category, body in rows])


@router.message(F.text == "📝 Заметки")
@router.callback_query(F.data == "notes:open")
async def notes_open(event: types.Message | types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    rows = list_notes(event.from_user.id)
    text = "📝 Ваши заметки:\n\n" + _render_notes(rows)
    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text, reply_markup=notes_keyboard())
        await event.answer()
    else:
        await event.answer(text, reply_markup=notes_keyboard())


@router.callback_query(F.data == "notes:add")
async def notes_add_start(callback: types.CallbackQuery) -> None:
    await callback.message.edit_text("Выберите способ добавления заметки:", reply_markup=add_mode_keyboard())
    await callback.answer()


@router.callback_query(F.data == "notes:add:new")
async def notes_add_new_category(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Введите название новой категории:")
    await state.set_state(NoteStates.new_category)
    await callback.answer()


@router.callback_query(F.data == "notes:add:existing")
async def notes_add_existing_category(callback: types.CallbackQuery, state: FSMContext) -> None:
    categories = list_categories(callback.from_user.id)
    if not categories:
        await callback.message.answer("Категорий пока нет. Сначала создайте новую категорию.")
        await callback.answer()
        return

    await state.update_data(categories_map={title: category_id for category_id, title in categories})
    await callback.message.answer(
        "Выберите категорию (default keyboard):",
        reply_markup=categories_keyboard([title for _, title in categories]),
    )
    await state.set_state(NoteStates.choose_existing_category)
    await callback.answer()


@router.callback_query(F.data == "notes:cancel")
async def notes_cancel(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.answer("Действие отменено.", reply_markup=main_menu())
    await callback.answer()


@router.message(NoteStates.new_category)
async def notes_create_category(message: types.Message, state: FSMContext) -> None:
    category_id = create_category(message.from_user.id, message.text.strip())
    await state.update_data(category_id=category_id)
    await message.answer("Введите текст заметки:")
    await state.set_state(NoteStates.note_body)


@router.message(NoteStates.choose_existing_category)
async def notes_choose_category(message: types.Message, state: FSMContext) -> None:
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Действие отменено.", reply_markup=main_menu())
        return

    data = await state.get_data()
    category_map = data.get("categories_map", {})
    category_id = category_map.get(message.text)
    if not category_id:
        await message.answer("Выберите категорию кнопкой ниже.")
        return

    await state.update_data(category_id=category_id)
    await message.answer("Введите текст заметки:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(NoteStates.note_body)


@router.message(NoteStates.note_body)
async def notes_save(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    add_note(message.from_user.id, data.get("category_id"), message.text.strip())
    await state.clear()
    await message.answer("✅ Заметка сохранена.", reply_markup=notes_keyboard())


@router.callback_query(F.data == "notes:delete")
async def notes_delete_start(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Введите ID заметки для удаления:")
    await state.set_state(NoteStates.delete_note)
    await callback.answer()


@router.message(NoteStates.delete_note)
async def notes_delete_finish(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("ID должен быть числом.")
        return

    ok = delete_note(message.from_user.id, int(message.text))
    await state.clear()
    await message.answer("✅ Заметка удалена." if ok else "Заметка не найдена.", reply_markup=notes_keyboard())
