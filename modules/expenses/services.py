from __future__ import annotations

from decimal import Decimal

from core.db_settings import execute_query
from modules.users.services import ensure_user_exists


def add_expense(user_id: int, amount: Decimal, category: str) -> None:
    ensure_user_exists(user_id, None)
    execute_query(
        """
        INSERT INTO expenses (user_id, amount, category)
        VALUES (%s, %s, %s)
        """,
        (user_id, amount, category),
    )


def get_month_expenses(user_id: int) -> list[tuple]:
    return execute_query(
        """
        SELECT id, category, amount, created_at
        FROM expenses
        WHERE user_id = %s
          AND date_trunc('month', created_at) = date_trunc('month', CURRENT_DATE)
        ORDER BY created_at DESC
        """,
        (user_id,),
        fetch="all",
    ) or []


def delete_expense_last_month(user_id: int, expense_id: int) -> bool:
    result = execute_query(
        """
        DELETE FROM expenses
        WHERE user_id = %s
          AND id = %s
          AND date_trunc('month', created_at) = date_trunc('month', CURRENT_DATE)
        RETURNING id
        """,
        (user_id, expense_id),
        fetch="one",
    )
    return bool(result)


def get_total_for_current_year(user_id: int) -> Decimal:
    row = execute_query(
        """
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE user_id = %s
          AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE)
        """,
        (user_id,),
        fetch="one",
    )
    return row["total"] if row else Decimal("0")


def get_total_for_all_time(user_id: int) -> Decimal:
    row = execute_query(
        """
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE user_id = %s
        """,
        (user_id,),
        fetch="one",
    )
    return row["total"] if row else Decimal("0")


def get_detailed_for_period(user_id: int, period: str) -> list[tuple]:
    if period == "year":
        query = """
            SELECT category, amount, created_at
            FROM expenses
            WHERE user_id = %s
              AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE)
            ORDER BY created_at DESC
        """
        params = (user_id,)
    else:
        query = """
            SELECT category, amount, created_at
            FROM expenses
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 100
        """
        params = (user_id,)

    return execute_query(query, params, fetch="all") or []
