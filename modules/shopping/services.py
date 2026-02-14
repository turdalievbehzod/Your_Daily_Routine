from core.db_settings import execute_query


def get_items(user_id: int) -> list[tuple]:
    return execute_query(
        "SELECT id, title, created_at FROM shopping_items WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
        fetch="all",
    ) or []


def add_item(user_id: int, title: str) -> None:
    execute_query(
        "INSERT INTO shopping_items (user_id, title) VALUES (%s, %s)",
        (user_id, title),
    )


def delete_item(user_id: int, item_id: int) -> bool:
    row = execute_query(
        "DELETE FROM shopping_items WHERE user_id = %s AND id = %s RETURNING id",
        (user_id, item_id),
        fetch="one",
    )
    return bool(row)
