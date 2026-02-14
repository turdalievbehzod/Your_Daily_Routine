from core.db_settings import execute_query


def get_or_create_user(user_id: int, username: str | None):
    user = execute_query(
        "SELECT id FROM users WHERE id = %s",
        (user_id,),
        fetch="one"
    )

    if not user:
        execute_query(
            "INSERT INTO users (id, username) VALUES (%s, %s)",
            (user_id, username)
        )


def ensure_user_exists(user_id: int, username: str | None) -> None:
    """Гарантирует наличие пользователя в БД, даже если он не нажимал /start."""
    get_or_create_user(user_id=user_id, username=username)
