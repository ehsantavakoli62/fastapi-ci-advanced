import sqlite3
import csv
import logging
from typing import List

# Database file name
# نام فایل دیتابیس
DB_NAME = 'homework.db'

def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    """
    Deletes incorrect fee records from table_fees based on the provided CSV file.
    رکورد جریمه‌های اشتباه را از جدول table_fees بر اساس فایل CSV داده شده حذف می‌کند.
    """
    
    wrong_fees_data: List[tuple] = []
    
    # 1. Read data from the CSV file (assuming format: date,car_number)
    # 1. خواندن داده‌ها از فایل CSV (با فرض فرمت: تاریخ، شماره خودرو)
    try:
        with open(wrong_fees_file, mode='r', encoding='utf-8') as file:
            # Skip the header row
            # رد کردن سطر هدر
            reader = csv.reader(file)
            next(reader) 
            
            for row in reader:
                # CSV row assumed to be [date, car_number, ...]
                # فرض می‌شود سطر CSV شامل [تاریخ، شماره خودرو، ...] باشد
                # We need (car_number, fee_date) for the DELETE query
                # ما به (شماره خودرو، تاریخ جریمه) برای کوئری DELETE نیاز داریم
                if len(row) >= 2:
                    # Note: Order for deletion query should be (car_number, fee_date)
                    # توجه: ترتیب برای کوئری حذف باید (شماره خودرو، تاریخ جریمه) باشد
                    wrong_fees_data.append((row[1].strip(), row[0].strip())) 
                
    except FileNotFoundError:
        logging.error(f"Error: CSV file '{wrong_fees_file}' not found.")
        return

    if not wrong_fees_data:
        logging.info("No wrong fees found in the CSV file. Nothing to delete.")
        return

    # 2. SQL DELETE query using parametrized values
    # 2. کوئری DELETE SQL با استفاده از مقادیر پارامتری
    sql_delete = """
    DELETE FROM 
        table_fees
    WHERE 
        car_number = ? AND fee_date = ?
    """
    
    # 3. Use executemany for efficiency
    # 3. استفاده از executemany برای کارایی
    try:
        cursor.executemany(sql_delete, wrong_fees_data)
        logging.info(f"Successfully deleted {cursor.rowcount} wrong fee records.")
    except sqlite3.Error as e:
        logging.error(f"Database error during deletion: {e}")

# --- Main for Demonstration ---
# --- بخش اصلی برای نمایش ---
def main():
    # NOTE: The wrong_fees.csv file must exist and homework.db must contain table_fees
    # توجه: فایل wrong_fees.csv باید وجود داشته باشد و homework.db باید شامل table_fees باشد
    
    # Create a dummy CSV file for demonstration if it doesn't exist
    # ایجاد یک فایل CSV ساختگی برای نمایش اگر وجود نداشته باشد
    DUMMY_CSV = 'wrong_fees.csv'
    dummy_data = [
        ['fee_date', 'car_number'],
        ['2023-10-25', 'X777XX77'],
        ['2023-10-26', 'Y888YY88'],
    ]
    with open(DUMMY_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(dummy_data)

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # Optional: insert dummy data to be deleted
        # اختیاری: درج داده‌های ساختگی برای حذف
        cursor.execute("CREATE TABLE IF NOT EXISTS table_fees (car_number TEXT, fee_date TEXT, amount REAL)")
        cursor.execute("INSERT INTO table_fees VALUES ('X777XX77', '2023-10-25', 1500.0)")
        cursor.execute("INSERT INTO table_fees VALUES ('Y888YY88', '2023-10-26', 1000.0)")
        conn.commit()
        
        delete_wrong_fees(cursor, DUMMY_CSV)
        
        # Check remaining data (optional)
        # بررسی داده‌های باقی‌مانده
        cursor.execute("SELECT COUNT(*) FROM table_fees")
        print(f"Remaining fees after deletion: {cursor.fetchone()[0]}")

if __name__ == '__main__':
    main()
