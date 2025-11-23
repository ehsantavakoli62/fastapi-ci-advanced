import sqlite3
import requests
import time
import logging
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool

# Basic logging configuration
# تنظیمات پایه لاگ
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
# ثابت‌ها
API_BASE_URL = "https://swapi.dev/api/people/"
DB_FILE = 'star_wars_pool_characters.db'
CHAR_IDS = list(range(1, 21)) # 20 characters to fetch

# --- Helper Functions (From previous task, simplified for pool usage) ---
# --- توابع کمکی (از وظیفه قبلی، ساده شده برای استفاده در Pool) ---

def setup_database(db_name: str):
    # Initializes the SQLite database and creates the table.
    # دیتابیس SQLite را مقداردهی اولیه می‌کند و جدول را ایجاد می‌کند.
    with sqlite3.connect(db_name) as conn:
        conn.execute("DROP TABLE IF EXISTS characters") # Ensure clean run
        conn.execute("""
            CREATE TABLE characters (
                id INTEGER PRIMARY KEY,
                name TEXT,
                height INTEGER,
                gender TEXT
            )
        """)
        conn.commit()
        
def fetch_and_save_character(character_id: int):
    # Fetches data and saves it to the DB. Designed to be run by pool workers.
    # داده‌ها را واکشی و در DB ذخیره می‌کند. طراحی شده برای اجرا توسط کارگران Pool.
    url = f"{API_BASE_URL}{character_id}/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract required fields (handling 'unknown' height)
        # استخراج فیلدهای مورد نیاز
        height = data.get('height')
        height = int(height) if height and height != 'unknown' else 0

        # Data for insertion
        # داده‌ها برای درج
        insert_data = (character_id, data.get('name', 'N/A'), height, data.get('gender', 'N/A'))

        # Insert data directly into the DB from the worker (Database access must be thread/process safe)
        # درج داده مستقیماً در DB از کارگر (دسترسی به دیتابیس باید ایمن باشد)
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO characters (id, name, height, gender) VALUES (?, ?, ?, ?)", insert_data)
            conn.commit()
            
        logger.debug(f"Saved character {character_id}.")
        return True # Return success status
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching character {character_id}: {e}")
        return False

# --- Pool Execution Functions ---
# --- توابع اجرای Pool ---

def pool_fetch_and_save(db_name: str, char_ids: list):
    """
    Fetches and saves character data using multiprocessing.Pool (Processes).
    داده‌های کاراکتر را با استفاده از Pool فرآیندها واکشی و ذخیره می‌کند.
    """
    logger.info("Starting multiprocessing.Pool (Process) execution...")
    setup_database(db_name)
    start_time = time.time()
    
    # Use max available cores
    # استفاده از حداکثر هسته‌های موجود
    num_processes = cpu_count()
    
    # Using Pool
    # استفاده از Pool
    with Pool(processes=num_processes) as pool:
        # map() applies the function to all items in the iterable
        # map() تابع را به تمام آیتم‌های تکرارپذیر اعمال می‌کند
        pool.map(fetch_and_save_character, char_ids)
        
    duration = round(time.time() - start_time, 2)
    logger.info(f"Process Pool finished in: {duration} seconds.")
    return duration

def thread_pool_fetch_and_save(db_name: str, char_ids: list):
    """
    Fetches and saves character data using multiprocessing.pool.ThreadPool (Threads).
    داده‌های کاراکتر را با استفاده از ThreadPool واکشی و ذخیره می‌کند.
    """
    logger.info("Starting multiprocessing.pool.ThreadPool (Thread) execution...")
    setup_database(db_name)
    start_time = time.time()

    # Use a large number of threads for I/O bound task
    # استفاده از تعداد زیادی نخ برای وظیفه محدود به I/O
    num_threads = 20
    
    # Using ThreadPool
    # استفاده از ThreadPool
    with ThreadPool(processes=num_threads) as pool:
        # map() applies the function to all items in the iterable
        # map() تابع را به تمام آیتم‌های تکرارپذیر اعمال می‌کند
        pool.map(fetch_and_save_character, char_ids)

    duration = round(time.time() - start_time, 2)
    logger.info(f"Thread Pool finished in: {duration} seconds.")
    return duration

# --- Main Function ---
# --- تابع اصلی ---
def main():
    # 1. Run Process Pool test
    time_proc_pool = pool_fetch_and_save(DB_FILE, CHAR_IDS)
    
    # 2. Run Thread Pool test
    time_thread_pool = thread_pool_fetch_and_save(DB_FILE, CHAR_IDS)
    
    logger.info(f"\n--- Final Comparison ---")
    logger.info(f"Process Pool Time: {time_proc_pool} seconds")
    logger.info(f"Thread Pool Time: {time_thread_pool} seconds")
    
    # Expected result: Thread Pool is faster because the task is I/O-bound (network requests).
    # نتیجه مورد انتظار: Thread Pool سریع‌تر است زیرا وظیفه محدود به I/O است (درخواست‌های شبکه).
    logger.info("Conclusion: ThreadPool is expected to be faster for this I/O-bound task due to GIL release during waiting (network I/O).")
    
if __name__ == '__main__':
    main()
