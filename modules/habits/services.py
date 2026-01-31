from core.db_settings import execute_query


def add_habit(user_id: int, name: str, frequency: str):
    execute_query(
        """
        INSERT INTO habits (user_id, name, frequency)
        VALUES (%s, %s, %s)
        """,
        (user_id, name, frequency)
    )
