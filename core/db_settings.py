from __future__ import annotations

from typing import Any, Optional, Union

import psycopg2
from psycopg2.extras import DictCursor, DictRow

from core.config import DB_CONFIG


class DatabaseManager:
    """Context manager для работы с PostgreSQL."""

    def __init__(self) -> None:
        self.conn: Optional[psycopg2.extensions.connection] = None
        self.cursor: Optional[psycopg2.extensions.cursor] = None

    def __enter__(self) -> "DatabaseManager":
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()

        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute(self, query: str, params: Union[tuple, dict, None] = None) -> None:
        assert self.cursor is not None
        self.cursor.execute(query, params)

    def fetchone(self, query: str, params: Union[tuple, dict, None] = None) -> Optional[DictRow]:
        assert self.cursor is not None
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetchall(self, query: str, params: Union[tuple, dict, None] = None) -> list[tuple[Any, ...]]:
        assert self.cursor is not None
        self.cursor.execute(query, params)
        return self.cursor.fetchall()


def execute_query(
    query: str,
    params: Union[tuple, dict, None] = None,
    fetch: Union[str, None] = None,
) -> DictRow | None | list[tuple[Any, ...]] | bool:
    with DatabaseManager() as db:
        if fetch == "one":
            return db.fetchone(query=query, params=params)
        if fetch == "all":
            return db.fetchall(query=query, params=params)

        db.execute(query=query, params=params)
        return True
