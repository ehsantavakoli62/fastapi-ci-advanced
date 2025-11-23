# db_init.py
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
DB_NAME = 'practise_rest.db'

def init_db(db_name=DB_NAME):
    """Initializes the database with normalized Author and Book tables."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("DROP TABLE IF EXISTS Book;")
    cursor.execute("DROP TABLE IF EXISTS Author;")

    # ایجاد جدول Author
    cursor.execute("""
        CREATE TABLE Author (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            middle_name TEXT
        );
    """)

    # ایجاد جدول Book (با ON DELETE CASCADE برای حذف آبشاری کتاب‌ها هنگام حذف نویسنده)
    cursor.execute("""
        CREATE TABLE Book (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_name TEXT NOT NULL,
            publish_year INTEGER NOT NULL,
            ISBN TEXT NOT NULL UNIQUE,
            author_id INTEGER NOT NULL,
            
            FOREIGN KEY (author_id)
                REFERENCES Author (id)
                ON DELETE CASCADE
        );
    """)
    
    # درج داده‌های نمونه
    cursor.execute("INSERT INTO Author (first_name, last_name) VALUES ('Федор', 'Достоевский')")
    dostoevsky_id = cursor.lastrowid
    
    cursor.execute("""
        INSERT INTO Book (book_name, publish_year, ISBN, author_id)
        VALUES 
            ('Преступление и наказание', 1866, '978-5-040985536', ?);
    """, (dostoevsky_id,))

    conn.commit()
    conn.close()
    logging.info(f"Database {DB_NAME} initialized.")

if __name__ == '__main__':
    init_db()
