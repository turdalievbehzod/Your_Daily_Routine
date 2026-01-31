from core.db_settings import execute_query


def add_item(user_id: int, title: str):
    execute_query(
        """
        INSERT INTO shopping_items (user_id, title)
        VALUES (%s, %s)
        """,
        (user_id, title)
    )
