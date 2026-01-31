from pathlib import Path
from core.db_settings import execute_query


def init_db():
    schema_path = Path("database/schema.sql")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = f.read()

    for statement in schema.split(";"):
        stmt = statement.strip()
        if stmt:
            execute_query(stmt)
