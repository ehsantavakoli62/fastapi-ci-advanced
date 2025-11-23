# db_init.py

import sqlite3
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

DB_NAME = 'practise_api.db'

def init_db():
    """
    Initializes the database, creating the 'rooms' table.
    دیتابیس را مقداردهی اولیه می‌کند و جدول 'rooms' را ایجاد می‌کند.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            
            # Drop table if exists to ensure a clean start
            # حذف جدول در صورت وجود برای اطمینان از شروعی تمیز
            cursor.execute("DROP TABLE IF EXISTS rooms;")
            
            # Create the rooms table with a status field (booked/available)
            # ایجاد جدول اتاق‌ها با فیلد وضعیت (رزرو شده/در دسترس)
            cursor.execute("""
                CREATE TABLE rooms (
                    roomId INTEGER PRIMARY KEY AUTOINCREMENT,
                    floor INTEGER NOT NULL,
                    guestNum INTEGER NOT NULL,
                    beds INTEGER NOT NULL,
                    price INTEGER NOT NULL,
                    is_available BOOLEAN NOT NULL DEFAULT 1 
                );
            """)
            
            # Insert initial data corresponding to the test requirements
            # درج داده‌های اولیه مطابق با الزامات تست
            initial_rooms: List[Dict[str, Any]] = [
                {"floor": 2, "guestNum": 1, "beds": 1, "price": 2000, "is_available": 1},
                {"floor": 1, "guestNum": 2, "beds": 1, "price": 2500, "is_available": 1},
                # Additional rooms for robustness
                {"floor": 3, "guestNum": 4, "beds": 2, "price": 4500, "is_available": 1},
            ]
            
            cursor.executemany("""
                INSERT INTO rooms (floor, guestNum, beds, price, is_available)
                VALUES (:floor, :guestNum, :beds, :price, :is_available);
            """, initial_rooms)
            
            conn.commit()
            logging.info(f"Database '{DB_NAME}' initialized successfully with 'rooms' table.")
            
    except sqlite3.Error as e:
        logging.error(f"Database error during initialization: {e}")

if __name__ == '__main__':
    init_db()
