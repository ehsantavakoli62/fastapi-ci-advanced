import sqlite3
import logging
import datetime
from typing import List, Dict, Set, Tuple

# Database file name
# نام فایل دیتابیس
DB_NAME = 'homework.db'

# Mapping of day index (0=Monday, 6=Sunday) to training sport
# نگاشت شاخص روز (۰=دوشنبه، ۶=یکشنبه) به ورزش تمرینی
DAY_TO_SPORT: Dict[int, str] = {
    0: 'Футбол',      # Monday
    1: 'Хоккей',      # Tuesday
    2: 'Шахматы',     # Wednesday
    3: 'SUP-сёрфинг', # Thursday
    4: 'Бокс',        # Friday
    5: 'Dota2',       # Saturday
    6: 'Шахбокс',     # Sunday
}

# Number of total employees and shift size
# تعداد کل کارمندان و اندازه شیفت
TOTAL_EMPLOYEES = 366
SHIFT_SIZE = 10
NUM_DAYS = 366 # For simplicity, assuming a non-leap year schedule

def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    """
    Updates the work schedule to ensure no employee is scheduled on their training day.
    برنامه کاری را به روز می‌کند تا اطمینان حاصل شود که هیچ کارمندی در روز تمرین خود برنامه‌ریزی نشده است.
    """
    
    # 1. Define/setup table_employees (Employee ID to Sport mapping)
    # 1. تعریف/تنظیم table_employees (نگاشت شناسه کارمند به ورزش)
    
    # We must ensure all 366 employees are mapped to a sport.
    # باید اطمینان حاصل کنیم که تمام ۳۶۶ کارمند به یک ورزش نگاشت شده‌اند.
    sports_list = list(DAY_TO_SPORT.values())
    employee_sports: Dict[int, str] = {}
    
    # For simplicity, assign sports cyclically
    # برای سادگی، ورزش‌ها را به صورت چرخه‌ای اختصاص می‌دهیم
    for emp_id in range(1, TOTAL_EMPLOYEES + 1):
        employee_sports[emp_id] = sports_list[(emp_id - 1) % len(sports_list)]

    # Assuming table_employees is available (inserting if not present):
    # فرض می‌کنیم table_employees در دسترس است (درج در صورت عدم وجود):
    cursor.execute("DROP TABLE IF EXISTS table_employees")
    cursor.execute("CREATE TABLE table_employees (employee_id INTEGER PRIMARY KEY, sport TEXT NOT NULL)")
    cursor.executemany("INSERT INTO table_employees VALUES (?, ?)", employee_sports.items())

    # 2. Delete existing schedule and create new one
    # 2. حذف برنامه موجود و ایجاد برنامه جدید
    cursor.execute("DROP TABLE IF EXISTS table_friendship_schedule")
    cursor.execute("""
        CREATE TABLE table_friendship_schedule (
            day_of_year INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            PRIMARY KEY (day_of_year, employee_id)
        )
    """)
    
    # 3. Create the new schedule
    # 3. ایجاد برنامه جدید
    schedule_data: List[Tuple[int, int]] = []
    
    # All employees are initially available
    # همه کارمندان در ابتدا در دسترس هستند
    available_employees: Set[int] = set(range(1, TOTAL_EMPLOYEES + 1))
    
    # Start date (e.g., Jan 1st of a common year)
    # تاریخ شروع (مثلاً ۱ ژانویه یک سال معمولی)
    start_date = datetime.date(2023, 1, 1) # A non-leap year
    
    # List of employee IDs, shuffled for random selection
    # لیست شناسه‌های کارمندان، به هم ریخته برای انتخاب تصادفی
    employee_ids = list(available_employees) 
    random.shuffle(employee_ids)

    # Re-map employee_sports for faster lookup
    # نگاشت مجدد employee_sports برای جستجوی سریعتر
    # Fetching from DB is also an option but memory lookup is faster for this algorithm
    # واکشی از DB نیز یک گزینه است، اما جستجوی حافظه برای این الگوریتم سریعتر است
    cursor.execute("SELECT employee_id, sport FROM table_employees")
    db_employee_sports = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Simple algorithm: iterate days and find 10 available employees
    # الگوریتم ساده: تکرار روزها و یافتن ۱۰ کارمند در دسترس
    for day_index in range(NUM_DAYS):
        current_date = start_date + datetime.timedelta(days=day_index)
        day_of_week = current_date.weekday() # 0=Monday, 6=Sunday
        day_of_year = day_index + 1
        training_sport = DAY_TO_SPORT.get(day_of_week)
        
        # 3.1. Find eligible employees for this day
        # 3.1. یافتن کارمندان واجد شرایط برای این روز
        eligible_employees: List[int] = []
        for emp_id in employee_ids:
            if db_employee_sports.get(emp_id) != training_sport:
                eligible_employees.append(emp_id)
        
        # 3.2. Select SHIFT_SIZE employees from the eligible list
        # 3.2. انتخاب SHIFT_SIZE کارمند از لیست واجد شرایط
        selected_shift = eligible_employees[:SHIFT_SIZE]
        
        if len(selected_shift) < SHIFT_SIZE:
             logging.warning(f"Warning: Could only schedule {len(selected_shift)} employees on day {day_of_year} (Training: {training_sport}).")

        for emp_id in selected_shift:
            schedule_data.append((day_of_year, emp_id))
            
        # 3.3. Rotate the list of employees to ensure fair distribution over time
        # 3.3. چرخاندن لیست کارمندان برای اطمینان از توزیع عادلانه در طول زمان
        if selected_shift:
            # Move selected employees to the end of the list to prioritize others next time
            # انتقال کارمندان انتخاب شده به انتهای لیست برای اولویت دادن به دیگران در نوبت بعدی
            employee_ids = [e for e in employee_ids if e not in selected_shift] + selected_shift
        
    # 4. Insert the new schedule
    # 4. درج برنامه جدید
    cursor.executemany("INSERT INTO table_friendship_schedule VALUES (?, ?)", schedule_data)
    
    logging.info(f"Successfully generated new schedule for {NUM_DAYS} days.")

# --- Main for Demonstration ---
# --- بخش اصلی برای نمایش ---
def main():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        update_work_schedule(cursor)
        conn.commit()
        
        # Verify (optional)
        # تأیید (اختیاری)
        cursor.execute("SELECT COUNT(DISTINCT employee_id) FROM table_friendship_schedule")
        active_workers = cursor.fetchone()[0]
        print(f"Number of distinct workers used: {active_workers}/{TOTAL_EMPLOYEES}")

if __name__ == '__main__':
    main()
