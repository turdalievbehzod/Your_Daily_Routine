import asyncio
from aiogram import Bot, Dispatcher

from core.config import BOT_TOKEN
from core.db_init import init_db

from modules.users.handlers import router as users_router
from modules.tasks.handlers import router as tasks_router
from modules.expenses.handlers import router as expenses_router
from modules.habits.handlers import router as habits_router
from modules.shopping.handlers import router as shopping_router


async def main():
    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(users_router)
    dp.include_router(tasks_router)
    dp.include_router(expenses_router)
    dp.include_router(habits_router)
    dp.include_router(shopping_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
