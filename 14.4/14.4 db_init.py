# db_init.py

import sqlite3
import logging

# Basic logging configuration (تنظیمات پایه لاگ)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Database file name (نام فایل دیتابیس)
DB_NAME = 'practise.db'

def init_db():
    """
    Initializes the database, creating the books table with the new views_count field.
    دیتابیس را مقداردهی اولیه می‌کند و جدول کتاب‌ها را با فیلد جدید views_count ایجاد می‌کند.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            
            # Drop table if it exists to ensure a clean start
            # حذف جدول در صورت وجود برای اطمینان از شروعی تمیز
            cursor.execute("DROP TABLE IF EXISTS table_books;")
            
            # Create the table with the required fields, including the new 'views_count' (Task 4)
            # ایجاد جدول با فیلدهای مورد نیاز، از جمله 'views_count' جدید (وظیفه ۴)
            cursor.execute("""
                CREATE TABLE table_books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_name TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publish_year INTEGER NOT NULL,
                    ISBN TEXT NOT NULL UNIQUE,
                    views_count INTEGER NOT NULL DEFAULT 0
                );
            """)
            
            # Insert some initial data for testing (درج داده‌های اولیه برای تست)
            cursor.executemany("""
                INSERT INTO table_books (book_name, author, publish_year, ISBN)
                VALUES (?, ?, ?, ?);
            """, [
                ("Война и мир", "Лев Толстой", 1869, "978-5-17-068393-3"),
                ("Преступление и наказание", "Федор Достоевский", 1866, "978-5-04-098553-6"),
                ("Идиот", "Федор Достоевский", 1869, "978-5-17-080353-8"),
                ("Мастер и Маргарита", "Михаил Булгаков", 1967, "978-5-17-063943-5")
            ])
            
            conn.commit()
            logging.info("Database 'practise.db' initialized successfully with 'table_books'.")
            
    except sqlite3.Error as e:
        logging.error(f"Database error during initialization: {e}")

if __name__ == '__main__':
    init_db()
