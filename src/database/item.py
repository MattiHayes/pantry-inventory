import sqlite3

from .utils import delete_row_from_db, get_connection, get_row_from_db, rename_row_in_db


def item_exists_in_cupboard(name: str, cupboard_id: int) -> bool:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT 1
            FROM items
            WHERE name = ? AND cupboard_id = ?
            """,
            (name, cupboard_id)
        ).fetchone()
    return row is not None


def insert_item(name: str, quantity: float, unit: str, cupboard_id: int) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            """
                INSERT INTO items (name, quantity, unit, cupboard_id)
                VALUES (?, ?, ?, ?)
            """,
            (name, quantity, unit, cupboard_id)
        )
        connection.commit()
    id = cursor.lastrowid
    return id

def get_item(item_id: int) -> sqlite3.Row | None:
    return get_row_from_db("items", item_id)

def rename_item(item_id: int, name: str) -> None:
    rename_row_in_db("items", item_id, name)

def remove_item(item_id: int) -> None:
    delete_row_from_db("items", item_id)

def get_item_with_name_in_cupboard(item_name: str, cubboard_id: int) -> sqlite3.Row | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, name, quantity, unit, cupboard_id
            FROM items
            WHERE name = ? AND cupboard_id = ?
            """,
            (item_name, cubboard_id)
        ).fetchone()
    return row

def update_item_quantity(item_id: int, quantity: float) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE items
            SET quantity = ?
            WHERE id = ?
            """,
            (quantity, item_id)
        )

        connection.commit()

def change_item_unit(item_id: int, unit: str) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE items
            SET unit = ?
            WHERE id = ?
            """,
            (unit, item_id)
        )
        connection.commit()
