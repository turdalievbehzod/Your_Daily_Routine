from aiogram import Router, types
from modules.users.services import get_or_create_user
from modules.menu.keyboards import main_menu

router = Router()


@router.message(commands=["start"])
async def start_handler(message: types.Message):
    get_or_create_user(
        user_id=message.from_user.id,
        username=message.from_user.username
    )

    await message.answer(
        "👋 Добро пожаловать в *Your Daily Routine*",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

@router.message(commands=["menu"])
async def menu_handler(message: types.Message):
    await message.answer(
        "🏠 Главное меню",
        reply_markup=main_menu()
    )
