import asyncio
import contextlib

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import BOT_TOKEN
from core.db_init import init_db
from core.logging_setup import setup_logging
from modules.expenses.handlers import router as expenses_router
from modules.habits.handlers import router as habits_router
from modules.habits.reminders import run_habit_reminders
from modules.shopping.handlers import router as shopping_router
from modules.tasks.handlers import router as tasks_router
from modules.users.handlers import router as users_router


async def main() -> None:
    logger = setup_logging()
    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(users_router)
    dp.include_router(expenses_router)
    dp.include_router(habits_router)
    dp.include_router(shopping_router)
    dp.include_router(tasks_router)

    reminder_task = asyncio.create_task(run_habit_reminders(bot))
    logger.info("Bot started")

    try:
        await dp.start_polling(bot)
    except Exception as exc:
        logger.exception("Fatal polling error: %s", exc)
    finally:
        reminder_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await reminder_task
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
