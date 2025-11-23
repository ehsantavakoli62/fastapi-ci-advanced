import sqlite3
import logging

# Database file name
# نام فایل دیتابیس
DB_NAME = 'homework.db'

# Name constant for Ivan Sovin
# ثابت نام برای ایوان سووین
IVAN_SOVIN_NAME = "Иван Совин" 

def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
        name: str,
) -> None:
    """
    Increases employee salary by 10% if it doesn't exceed Ivan Sovin's salary, 
    otherwise deletes the employee record. Ivan Sovin is not affected.
    حقوق کارمند را ۱۰٪ افزایش می‌دهد اگر از حقوق ایوان سووین تجاوز نکند، در غیر این صورت 
    رکورد کارمند را حذف می‌کند. ایوان سووین تحت تأثیر قرار نمی‌گیرد.
    """
    
    if name == IVAN_SOVIN_NAME:
        logging.info("Cannot modify the effective manager himself.")
        return

    # 1. Get Ivan Sovin's salary and the target employee's current salary
    # 1. دریافت حقوق ایوان سووین و حقوق فعلی کارمند هدف
    
    # We use a subquery/CTE approach to get both salaries efficiently, or two separate queries.
    # Two separate queries for clarity and error handling:
    
    # Get Ivan's salary
    # دریافت حقوق ایوان
    cursor.execute("SELECT salary FROM table_effective_manager WHERE name = ?", (IVAN_SOVIN_NAME,))
    ivan_salary_result = cursor.fetchone()
    if not ivan_salary_result:
        logging.error(f"Error: Ivan Sovin ('{IVAN_SOVIN_NAME}') not found in the table.")
        return
    ivan_salary = ivan_salary_result[0]
    
    # Get target employee's salary
    # دریافت حقوق کارمند هدف
    cursor.execute("SELECT salary FROM table_effective_manager WHERE name = ?", (name,))
    employee_salary_result = cursor.fetchone()
    if not employee_salary_result:
        logging.info(f"Employee '{name}' not found. No action taken.")
        return
    employee_salary = employee_salary_result[0]
    
    # 2. Calculate new salary
    # 2. محاسبه حقوق جدید
    new_salary = round(employee_salary * 1.10, 2)
    
    # 3. Decision and action
    # 3. تصمیم و اقدام
    if new_salary <= ivan_salary:
        # Action: Increase salary
        # اقدام: افزایش حقوق
        sql_update = "UPDATE table_effective_manager SET salary = ? WHERE name = ?"
        cursor.execute(sql_update, (new_salary, name))
        logging.info(f"Salary for '{name}' increased to {new_salary}. New salary <= Ivan's salary.")
    else:
        # Action: Fire employee (DELETE record)
        # اقدام: اخراج کارمند (حذف رکورد)
        sql_delete = "DELETE FROM table_effective_manager WHERE name = ?"
        cursor.execute(sql_delete, (name,))
        logging.warning(f"Employee '{name}' fired. New salary ({new_salary}) > Ivan's salary ({ivan_salary}).")

# --- Main for Demonstration ---
# --- بخش اصلی برای نمایش ---
def main():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # 1. Setup table
        # 1. تنظیم جدول
        cursor.execute("DROP TABLE IF EXISTS table_effective_manager")
        cursor.execute("""
            CREATE TABLE table_effective_manager (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                salary REAL NOT NULL
            )
        """)
        # Insert test data: Ivan and two employees (one eligible for raise, one not)
        # درج داده‌های تست: ایوان و دو کارمند (یکی واجد شرایط افزایش، دیگری نه)
        cursor.executemany("INSERT INTO table_effective_manager (name, salary) VALUES (?, ?)", [
            (IVAN_SOVIN_NAME, 50000.00),
            ('Peter Ivanov', 45000.00), # Eligible: 45000 * 1.1 = 49500 <= 50000
            ('Maria Petrova', 45500.00), # Not Eligible: 45500 * 1.1 = 50050 > 50000
        ])
        conn.commit()
        
        # 2. Test
        # 2. تست
        ivan_sovin_the_most_effective(cursor, 'Peter Ivanov')
        ivan_sovin_the_most_effective(cursor, 'Maria Petrova')
        
        # Check the results
        # بررسی نتایج
        cursor.execute("SELECT name, salary FROM table_effective_manager")
        print("\nFinal records:")
        for row in cursor.fetchall():
            print(row)

if __name__ == '__main__':
    main()
