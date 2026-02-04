import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import BOT_TOKEN

from modules.users.handlers import router as users_router
from modules.expenses.handlers import router as expenses_router
from modules.habits.handlers import router as habits_router
from modules.shopping.handlers import router as shopping_router
from modules.tasks.handlers import router as tasks_router


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем все роутеры
    dp.include_router(users_router)
    dp.include_router(expenses_router)
    dp.include_router(habits_router)
    dp.include_router(shopping_router)
    dp.include_router(tasks_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
