import sqlite3
import logging
from typing import List

# Database file name
# نام فایل دیتابیس
DB_NAME = 'homework.db'

# Define the acceptable temperature range (T = -18 ± 2)
# تعریف محدوده دمای قابل قبول
MIN_TEMP = -20  # -18 - 2
MAX_TEMP = -16  # -18 + 2
SPOIL_THRESHOLD = 3 # Number of hours outside range to be spoiled

def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    """
    Checks if the vaccine in a specific truck has spoiled by checking if 
    the temperature was outside the range [-20, -16] for 3 or more hours.
    بررسی می‌کند که آیا واکسن در یک کامیون خاص با بررسی اینکه دما به مدت ۳ ساعت یا بیشتر 
    خارج از محدوده [-۲۰، -۱۶] بوده است، فاسد شده است یا خیر.
    """
    
    # SQL query to count the number of temperature readings that are outside the acceptable range.
    # کوئری SQL برای شمارش تعداد خوانش‌های دما که خارج از محدوده قابل قبول هستند.
    sql_query = """
    SELECT 
        COUNT(*) 
    FROM 
        table_truck_with_vaccine
    WHERE 
        truck_number = ? AND (temperature < ? OR temperature > ?)
    """
    
    # Execute the query using parametrized query
    # اجرای کوئری با استفاده از پرس‌وجوی پارامتری
    cursor.execute(sql_query, (truck_number, MIN_TEMP, MAX_TEMP))
    
    # Fetch the count
    # واکشی تعداد
    spoiled_hours = cursor.fetchone()[0]
    
    # Check if the spoiled hours meet the threshold
    # بررسی اینکه آیا ساعات فاسد شده به حد نصاب می‌رسد
    return spoiled_hours >= SPOIL_THRESHOLD

# --- Main for Demonstration ---
# --- بخش اصلی برای نمایش (برای Skillbox لازم نیست، اما برای تست مفید است) ---
def main():
    # NOTE: Assume table_truck_with_vaccine is set up and populated in homework.db
    # توجه: فرض بر این است که جدول table_truck_with_vaccine در homework.db تنظیم و پر شده است
    
    # Example usage:
    # مثال استفاده:
    test_truck = 'A101'
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # NOTE: For a clean run, the database should be populated with test data here.
        # توجه: برای اجرای تمیز، دیتابیس باید در اینجا با داده‌های تستی پر شود.

        is_spoiled = check_if_vaccine_has_spoiled(cursor, test_truck)
        
        # This will only work if the table exists and contains data for A101
        # این فقط در صورتی کار می‌کند که جدول وجود داشته باشد و شامل داده‌هایی برای A101 باشد
        if is_spoiled:
            print(f"Vaccine in truck {test_truck} has SPOILED.")
        else:
            print(f"Vaccine in truck {test_truck} is OK.")

if __name__ == '__main__':
    main()
