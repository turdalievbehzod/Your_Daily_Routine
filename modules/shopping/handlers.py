from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from modules.menu.keyboards import main_menu
from modules.shopping.states import ShoppingStates
from modules.shopping.services import add_item

router = Router()


@router.message(lambda m: m.text == "🛒 Покупки")
async def shopping_start(message: types.Message, state: FSMContext):
    await message.answer("Что нужно купить?")
    await state.set_state(ShoppingStates.item)


@router.message(ShoppingStates.item)
async def shopping_add(message: types.Message, state: FSMContext):
    add_item(
        user_id=message.from_user.id,
        title=message.text
    )

    await message.answer("🛒 Добавлено в список", reply_markup=main_menu())
    await state.clear()
