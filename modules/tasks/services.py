from core.db_settings import execute_query


def create_task(user_id: int, title: str, deadline: str | None):
    execute_query(
        """
        INSERT INTO tasks (user_id, title, deadline)
        VALUES (%s, %s, %s)
        """,
        (user_id, title, deadline)
    )


def get_tasks(user_id: int):
    return execute_query(
        "SELECT * FROM tasks WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
        fetch="all"
    )
