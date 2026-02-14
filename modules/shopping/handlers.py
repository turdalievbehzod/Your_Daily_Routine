from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from modules.shopping.services import add_item, delete_item, get_items
from modules.shopping.states import ShoppingStates
from modules.users.services import ensure_user_exists

router = Router()


def shopping_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить в корзину", callback_data="shopping:add")],
            [InlineKeyboardButton(text="➖ Убрать с корзины", callback_data="shopping:delete")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main")],
        ]
    )


def _render_items(rows: list[tuple]) -> str:
    if not rows:
        return "В корзине пока нет желанных покупок."
    return "\n".join([f"• ID {item_id}: {title}" for item_id, title, _ in rows])


@router.message(F.text == "🛒 Шоппинг")
@router.callback_query(F.data == "shopping:open")
async def open_shopping(event: types.Message | types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    ensure_user_exists(event.from_user.id, event.from_user.username)
    rows = get_items(event.from_user.id)
    text = "🛒 Ваша корзина:\n\n" + _render_items(rows)
    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text, reply_markup=shopping_keyboard())
        await event.answer()
    else:
        await event.answer(text, reply_markup=shopping_keyboard())


@router.callback_query(F.data == "shopping:add")
async def start_add(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Введите название покупки:")
    await state.set_state(ShoppingStates.add_item)
    await callback.answer()


@router.message(ShoppingStates.add_item)
async def finish_add(message: types.Message, state: FSMContext) -> None:
    ensure_user_exists(message.from_user.id, message.from_user.username)
    add_item(message.from_user.id, message.text.strip())
    await state.clear()
    await message.answer("✅ Добавлено в корзину.", reply_markup=shopping_keyboard())


@router.callback_query(F.data == "shopping:delete")
async def start_delete(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Введите ID покупки для удаления:")
    await state.set_state(ShoppingStates.delete_item)
    await callback.answer()


@router.message(ShoppingStates.delete_item)
async def finish_delete(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("ID должен быть числом.")
        return
    ensure_user_exists(message.from_user.id, message.from_user.username)
    ok = delete_item(message.from_user.id, int(message.text))
    await state.clear()
    await message.answer(
        "✅ Покупка удалена." if ok else "Не найден товар с таким ID.",
        reply_markup=shopping_keyboard(),
    )
