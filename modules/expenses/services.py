from core.db_settings import execute_query


def add_expense(user_id: int, amount: float, category: str):
    execute_query(
        """
        INSERT INTO expenses (user_id, amount, category)
        VALUES (%s, %s, %s)
        """,
        (user_id, amount, category)
    )
