from .utils import get_connection
import sqlite3

def cupboard_exists(name: str) -> bool:
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT 1
        FROM cupboards
        WHERE name = ?
        """,
        (name,)
    )

    exists = cursor.fetchone() is not None

    connection.close()

    return exists


def insert_cupboard(name: str) -> int:
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO cupboards (name)
        VALUES (?)
        """,
        (name,)
    )
    connection.commit()
    id = cursor.lastrowid
    connection.close()
    print(f"Cupboard id = {id}")
    return id


def get_items_in_cupboard(cupboard_id: int) -> list[sqlite3.Row]:
    connection = get_connection()
    rows = connection.execute(
        """
        SELECT id, name, quantity, unit
        FROM items
        WHERE cupboard_id = ?
        """,
        (cupboard_id,)
    ).fetchall()
    connection.close()
    return rows

def get_cupboard_with_name(name: str) -> sqlite3.Row | None:
    connection = get_connection()
    row = connection.execute(
        """
        SELECT id, name
        FROM cupboards
        WHERE name = ?
        """,
        (name,)
    ).fetchone()
    connection.close()
    return row

def get_cupboard(cupboard_id: int) -> sqlite3.Row | None:
    connection = get_connection()
    row = connection.execute(
        """
        SELECT id, name, quantity, unit, cupboard_id
        FROM items
        WHERE id = ?
        """,
        (cupboard_id,)
    ).fetchone()
    connection.close()
    return row

def get_cupboards() -> list[sqlite3.Row]:
    connection = get_connection()
    rows = connection.execute(
        """
        SELECT *
        FROM cupboards
        """
    ).fetchall()
    connection.close()
    return rows