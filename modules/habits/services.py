from core.db_settings import execute_query


def list_habits(user_id: int) -> list[tuple]:
    return execute_query(
        """
        SELECT id, name, reminder_month, reminder_day, reminder_hour
        FROM habits
        WHERE user_id = %s
        ORDER BY id DESC
        """,
        (user_id,),
        fetch="all",
    ) or []


def add_habit(user_id: int, name: str, month: int, day: int, hour: int) -> None:
    execute_query(
        """
        INSERT INTO habits (user_id, name, reminder_month, reminder_day, reminder_hour)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (user_id, name, month, day, hour),
    )


def get_habit(user_id: int, habit_id: int):
    return execute_query(
        "SELECT id, name, reminder_month, reminder_day, reminder_hour FROM habits WHERE user_id = %s AND id = %s",
        (user_id, habit_id),
        fetch="one",
    )


def delete_habit(user_id: int, habit_id: int) -> bool:
    row = execute_query(
        "DELETE FROM habits WHERE user_id = %s AND id = %s RETURNING id",
        (user_id, habit_id),
        fetch="one",
    )
    return bool(row)


def update_habit(user_id: int, habit_id: int, name: str, month: int, day: int, hour: int) -> None:
    execute_query(
        """
        UPDATE habits
        SET name = %s, reminder_month = %s, reminder_day = %s, reminder_hour = %s
        WHERE user_id = %s AND id = %s
        """,
        (name, month, day, hour, user_id, habit_id),
    )


def due_habits(month: int, day: int, hour: int, year: int) -> list[tuple]:
    return execute_query(
        """
        SELECT id, user_id, name
        FROM habits
        WHERE reminder_month = %s
          AND reminder_day = %s
          AND reminder_hour = %s
          AND (last_notified_year IS NULL OR last_notified_year < %s)
        """,
        (month, day, hour, year),
        fetch="all",
    ) or []


def mark_notified(habit_id: int, year: int) -> None:
    execute_query(
        "UPDATE habits SET last_notified_year = %s WHERE id = %s",
        (year, habit_id),
    )
