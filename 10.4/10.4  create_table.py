import sqlite3


def create_car_table(db_name):
    # SQL command to create the table structure
    CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS table_car (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_number TEXT NOT NULL,
        car_name TEXT NOT NULL,
        description TEXT,
        belongs_to INTEGER,
        FOREIGN KEY (belongs_to) REFERENCES table_owner(id)
    );
    """

    conn = None
    try:
        # Connects to the database file
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(CREATE_TABLE_QUERY)
        conn.commit()
        print("✅ Table 'table_car' successfully prepared.")

    except sqlite3.Error as e:
        print(f"❌ Database Error: {e}")

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    DB_FILE = 'hw_1_database.db'
    create_car_table(DB_FILE)
