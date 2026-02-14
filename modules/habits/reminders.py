from __future__ import annotations

import asyncio
from datetime import datetime
import logging

from aiogram import Bot

from modules.habits.services import due_habits, mark_notified

logger = logging.getLogger("ydr")


async def run_habit_reminders(bot: Bot) -> None:
    while True:
        now = datetime.now()
        try:
            rows = due_habits(now.month, now.day, now.hour, now.year)
            for habit_id, user_id, name in rows:
                await bot.send_message(user_id, f"⏰ Пора заняться: {name}")
                mark_notified(habit_id, now.year)
                logger.info("Habit reminder sent to user_id=%s habit_id=%s", user_id, habit_id)
        except Exception as exc:
            logger.exception("Habit reminder loop error: %s", exc)

        await asyncio.sleep(60)
