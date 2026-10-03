import sqlite3

from .utils import delete_row_from_db, get_connection, get_row_from_db, rename_row_in_db


def cupboard_exists(name: str) -> bool:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT 1
            FROM cupboards
            WHERE name = ?
            """,
            (name,)
        )
        exists = cursor.fetchone() is not None
    return exists

def insert_cupboard(name: str) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO cupboards (name)
            VALUES (?)
            """,
            (name,)
        )
        connection.commit()
        id = cursor.lastrowid
    return id

def get_cupboard(cupboard_id: int) -> sqlite3.Row | None:
    return get_row_from_db("cupboards", cupboard_id)

def rename_cupboard(cupboard_id: int, name: str) -> None:
    rename_row_in_db("cupboards", cupboard_id, name)

def remove_cupboard(cupboard_id: int) -> None:
    delete_row_from_db("cupboards", cupboard_id)
    
def get_items_in_cupboard(cupboard_id: int) -> list[sqlite3.Row]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, name, quantity, unit
            FROM items
            WHERE cupboard_id = ?
            """,
            (cupboard_id,)
        ).fetchall()
    return rows

def get_cupboard_with_name(name: str) -> sqlite3.Row | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, name
            FROM cupboards
            WHERE name = ?
            """,
            (name,)
        ).fetchone()
    return row


def get_cupboards() -> list[sqlite3.Row]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM cupboards
            """
        ).fetchall()
    return rows
