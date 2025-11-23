# models.py

import sqlite3
from typing import List, Dict, Any, Optional
import logging

DB_NAME = 'practise_api.db'
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_db_connection() -> sqlite3.Connection:
    """Creates and returns a database connection (ایجاد و بازگرداندن اتصال دیتابیس)"""
    conn = sqlite3.connect(DB_NAME)
    # Set row_factory to sqlite3.Row for dictionary-like results
    # تنظیم row_factory به sqlite3.Row برای نتایج شبیه دیکشنری
    conn.row_factory = sqlite3.Row
    return conn

def get_all_available_rooms() -> List[Dict[str, Any]]:
    """Retrieves all available rooms from the database (بازیابی تمام اتاق‌های موجود)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Select only available rooms (انتخاب فقط اتاق‌های در دسترس)
    # Use parametrized query (استفاده از کوئری پارامتری)
    cursor.execute("SELECT * FROM rooms WHERE is_available = 1") 
    
    rooms = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rooms

def add_room(room_data: Dict[str, Any]) -> int:
    """Adds a new room to the database and returns its ID (افزودن اتاق جدید و بازگرداندن ID آن)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Use parametrized query (استفاده از کوئری پارامتری)
    cursor.execute(
        """
        INSERT INTO rooms (floor, guestNum, beds, price, is_available)
        VALUES (:floor, :guestNum, :beds, :price, 1)
        """,
        room_data
    )
    conn.commit()
    room_id = cursor.lastrowid
    conn.close()
    return room_id

def book_room_by_id(room_id: int) -> bool:
    """Sets a room as booked (is_available = 0). Returns True if updated, False otherwise (اتاق را رزرو می‌کند و وضعیت را برمی‌گرداند)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the room is already booked (بررسی اینکه آیا اتاق از قبل رزرو شده است)
    cursor.execute("SELECT is_available FROM rooms WHERE roomId = ?", (room_id,))
    room_status = cursor.fetchone()

    if room_status is None or room_status['is_available'] == 0:
        conn.close()
        return False # Room not found or already booked (اتاق یافت نشد یا قبلاً رزرو شده است)

    # Use parametrized query (استفاده از کوئری پارامتری)
    cursor.execute(
        "UPDATE rooms SET is_available = 0 WHERE roomId = ? AND is_available = 1", 
        (room_id,)
    )
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def get_room_status_by_id(room_id: int) -> Optional[int]:
    """Returns 1 if available, 0 if booked, or None if not found (وضعیت اتاق را برمی‌گرداند)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_available FROM rooms WHERE roomId = ?", (room_id,))
    result = cursor.fetchone()
    conn.close()
    return result['is_available'] if result else None
