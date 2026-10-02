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

if __name__ == "__main__":
    initialise_database()