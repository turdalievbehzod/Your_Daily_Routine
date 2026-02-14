from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from modules.menu.keyboards import main_menu
from modules.users.services import get_or_create_user

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message) -> None:
    get_or_create_user(user_id=message.from_user.id, username=message.from_user.username)
    await message.answer(
        "👋 Добро пожаловать в *Your Daily Routine*\nВыберите нужный инструмент в меню ниже.",
        reply_markup=main_menu(),
        parse_mode="Markdown",
    )


@router.message(Command("menu"))
async def menu_handler(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("🏠 Главное меню", reply_markup=main_menu())


@router.callback_query(F.data == "menu:main")
async def menu_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.answer("🏠 Главное меню", reply_markup=main_menu())
    await callback.answer()
