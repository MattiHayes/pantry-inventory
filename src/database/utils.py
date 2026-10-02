import sqlite3

DATABASE = "pantry.db"

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def initialise_database():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS cupboards (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )    
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            cupboard_id INTEGER NOT NULL,
            FOREIGN KEY (cupboard_id) REFERENCES cupboards(id)
        )
        """
    )

    connection.commit()
    connection.close()

def delete_row_from_db(db_name: str, id: int) -> None:
    connection = get_connection()

    connection.execute(
        f"""
        DELETE FROM {db_name}
        WHERE id = ?
        """,
        (id,)
    )
    connection.commit()
    connection.close()

def rename_row_in_db(db_name: str, id: int, name: str) -> None:
    connection = get_connection()
    connection.execute(
        f"""
        UPDATE {db_name}
        SET name = ?
        WHERE id = ?
        """,
        (name, id)
    )
    connection.commit()
    connection.close()

def get_row_from_db(db_name: str, id: int) -> sqlite3.Row:
    connection = get_connection()
    row = connection.execute(
        f"""
        SELECT *
        FROM {db_name}
        WHERE id = ?
        """,
        (id,)
    ).fetchone()
    connection.close()
    return row

if __name__ == "__main__":
    initialise_database()