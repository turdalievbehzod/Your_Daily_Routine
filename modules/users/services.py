from core.db_settings import execute_query


def get_or_create_user(user_id: int, username: str | None) -> bool:
    row = execute_query(
        """
        INSERT INTO users (id, username)
        VALUES (%s, %s)
        ON CONFLICT (id)
        DO UPDATE SET username = COALESCE(EXCLUDED.username, users.username)
        RETURNING id
        """,
        (user_id, username),
        fetch="one",
    )
    return bool(row)


def ensure_user_exists(user_id: int, username: str | None) -> bool:
    """Гарантирует наличие пользователя в БД, даже если он не нажимал /start."""
    return get_or_create_user(user_id=user_id, username=username)
