from core.db_settings import execute_query


def list_notes(user_id: int) -> list[tuple]:
    return execute_query(
        """
        SELECT n.id, COALESCE(c.title, 'Без категории') AS category, n.body
        FROM notes n
        LEFT JOIN note_categories c ON c.id = n.category_id
        WHERE n.user_id = %s
        ORDER BY n.created_at DESC
        """,
        (user_id,),
        fetch="all",
    ) or []


def list_categories(user_id: int) -> list[tuple]:
    return execute_query(
        "SELECT id, title FROM note_categories WHERE user_id = %s ORDER BY title",
        (user_id,),
        fetch="all",
    ) or []


def create_category(user_id: int, title: str) -> int:
    row = execute_query(
        """
        INSERT INTO note_categories (user_id, title)
        VALUES (%s, %s)
        ON CONFLICT (user_id, title)
        DO UPDATE SET title = EXCLUDED.title
        RETURNING id
        """,
        (user_id, title),
        fetch="one",
    )
    return int(row["id"])


def add_note(user_id: int, category_id: int | None, body: str) -> None:
    execute_query(
        "INSERT INTO notes (user_id, category_id, body) VALUES (%s, %s, %s)",
        (user_id, category_id, body),
    )


def delete_note(user_id: int, note_id: int) -> bool:
    row = execute_query(
        "DELETE FROM notes WHERE user_id = %s AND id = %s RETURNING id",
        (user_id, note_id),
        fetch="one",
    )
    return bool(row)
