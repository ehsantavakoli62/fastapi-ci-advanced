import sqlite3
import logging
import datetime

# Database file name
# نام فایل دیتابیس
DB_NAME = 'homework.db'

def check_if_such_bird_already_seen(
        cursor: sqlite3.Cursor,
        bird_name: str
) -> bool:
    """
    Checks if a bird with the given name already exists in the table_birds.
    بررسی می‌کند که آیا پرنده‌ای با نام داده شده قبلاً در table_birds وجود دارد.
    """
    
    # Using EXISTS which is generally more efficient than COUNT(*) > 0
    # استفاده از EXISTS که معمولاً کارآمدتر از COUNT(*) > 0 است
    sql_check = """
    SELECT 
        EXISTS (
            SELECT 
                1 
            FROM 
                table_birds 
            WHERE 
                bird_name = ?
        )
    """
    
    # Execute with parametrized query
    # اجرا با کوئری پارامتری
    cursor.execute(sql_check, (bird_name,))
    
    # The result is 1 (True) or 0 (False)
    # نتیجه ۱ (True) یا ۰ (False) است
    return cursor.fetchone()[0] == 1


def log_bird(
        cursor: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    """
    Inserts a new bird observation record into the table_birds.
    رکورد مشاهده پرنده جدید را در table_birds درج می‌کند.
    """
    
    sql_insert = """
    INSERT INTO 
        table_birds (bird_name, observation_time) 
    VALUES 
        (?, ?)
    """
    
    # Execute with parametrized query
    # اجرا با کوئری پارامتری
    cursor.execute(sql_insert, (bird_name, date_time))
    
    # Note: commit must be done by the caller (in main or context manager)
    # توجه: commit باید توسط فراخواننده انجام شود

# --- Main for Demonstration ---
# --- بخش اصلی برای نمایش ---
def main():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # 1. Setup table
        # 1. تنظیم جدول
        cursor.execute("DROP TABLE IF EXISTS table_birds")
        cursor.execute("""
            CREATE TABLE table_birds (
                id INTEGER PRIMARY KEY,
                observation_time TEXT NOT NULL,
                bird_name TEXT NOT NULL
            )
        """)
        conn.commit()

        # 2. Test
        # 2. تست
        bird1 = "Sparrow"
        bird2 = "Eagle"
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log the first bird
        # ثبت پرنده اول
        log_bird(cursor, bird1, current_time)
        print(f"Logged {bird1}.")
        
        # Check if bird1 is seen
        # بررسی اینکه آیا پرنده 1 دیده شده است
        print(f"Has seen {bird1}? {check_if_such_bird_already_seen(cursor, bird1)}")
        
        # Check if bird2 is seen (should be False)
        # بررسی اینکه آیا پرنده 2 دیده شده است (باید False باشد)
        print(f"Has seen {bird2}? {check_if_such_bird_already_seen(cursor, bird2)}")

        # Log the second bird
        # ثبت پرنده دوم
        log_bird(cursor, bird2, current_time)
        
        # Check if bird2 is now seen (should be True)
        # بررسی اینکه آیا پرنده 2 اکنون دیده شده است (باید True باشد)
        print(f"Has seen {bird2} now? {check_if_such_bird_already_seen(cursor, bird2)}")

if __name__ == '__main__':
    main()
