import sqlite3

DATABASE = "pantry.db"

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def initialise_database():
    with get_connection() as connection:
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
                FOREIGN KEY (cupboard_id) 
                    REFERENCES cupboards(id)
                    ON DELETE CASCADE
            )
            """
        )

        connection.commit()

def delete_row_from_db(db_name: str, id: int) -> None:
    with get_connection() as connection:
        connection.execute(
            f"""
            DELETE FROM {db_name}
            WHERE id = ?
            """,
            (id,)
        )
        connection.commit()

def rename_row_in_db(db_name: str, id: int, name: str) -> None:
    with get_connection() as connection:
        connection.execute(
            f"""
            UPDATE {db_name}
            SET name = ?
            WHERE id = ?
            """,
            (name, id)
        )
        connection.commit()

def get_row_from_db(db_name: str, id: int) -> sqlite3.Row:
    with get_connection() as connection:
        row = connection.execute(
            f"""
            SELECT *
            FROM {db_name}
            WHERE id = ?
            """,
            (id,)
        ).fetchone()
    return row

if __name__ == "__main__":
    initialise_database()