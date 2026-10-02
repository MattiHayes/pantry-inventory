from .utils import get_connection
import sqlite3

def item_exists_in_cupboard(name: str, cupboard_id: int) -> bool:
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT 1
        FROM items
        WHERE name = ? AND cupboard_id = ?
        """,
        (name, cupboard_id)
    )

    exists = cursor.fetchone() is not None

    connection.close()

    return exists


def insert_item(name: str, quantity: float, unit: str, cupboard_id: int) -> int:
    connection = get_connection()

    cursor = connection.execute(
        """
            INSERT INTO items (name, quantity, unit, cupboard_id)
            VALUES (?, ?, ?, ?)
        """,
        (name, quantity, unit, cupboard_id)
    )
    connection.commit()
    id = cursor.lastrowid
    connection.close()
    return id


def get_item(item_id: int) -> sqlite3.Row | None:
    connection = get_connection()

    row = connection.execute(
        """
        SELECT id, name, quantity, unit, cupboard_id
        FROM items
        WHERE id = ?
        """,
        (item_id,)
    ).fetchone()

    connection.close()

    return row

def get_item_with_name_in_cupboard(item_name: str, cubboard_id: int) -> sqlite3.Row | None:
    connection = get_connection()

    row = connection.execute(
        """
        SELECT id, name, quantity, unit, cupboard_id
        FROM items
        WHERE name = ? AND cupboard_id = ?
        """,
        (item_name, cubboard_id)
    ).fetchone()

    connection.close()

    return row

def update_item_quantity(item_id: int, quantity: float) -> None:
    connection = get_connection()

    connection.execute(
        """
        UPDATE items
        SET quantity = ?
        WHERE id = ?
        """,
        (quantity, item_id)
    )

    connection.commit()
    connection.close()

def rename_item(item_id: int, name: str) -> None:
    connection = get_connection()

    connection.execute(
        """
        UPDATE items
        SET name = ?
        WHERE id = ?
        """,
        (name, item_id)
    )

    connection.commit()
    connection.close()