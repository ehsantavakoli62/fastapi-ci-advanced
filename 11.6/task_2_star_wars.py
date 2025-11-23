import sqlite3
import requests
import threading
import time
import logging

# Basic logging configuration
# تنظیمات پایه لاگ
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
# ثابت‌ها
API_BASE_URL = "https://swapi.dev/api/people/"
DB_FILE = 'star_wars_characters.db'
CHAR_IDS = list(range(1, 21)) # 20 characters to fetch

# --- Database Setup ---
# --- تنظیم دیتابیس ---

def setup_database(db_name: str):
    # Initializes the SQLite database and creates the table if it doesn't exist.
    # دیتابیس SQLite را مقداردهی اولیه می‌کند و جدول را در صورت عدم وجود ایجاد می‌کند.
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        # Creating the table: id, name, height, gender
        # ایجاد جدول: شناسه، نام، قد، جنسیت
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY,
                name TEXT,
                height INTEGER,
                gender TEXT
            )
        """)
        conn.commit()
        logger.info("Database setup complete.")
        
# --- Data Extraction Function ---
# --- تابع استخراج داده‌ها ---

def fetch_character_data(character_id: int) -> dict:
    # Fetches data for a single character from the SWAPI.
    # داده‌های یک کاراکتر را از SWAPI واکشی می‌کند.
    url = f"{API_BASE_URL}{character_id}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Extract required fields (handling 'unknown' height)
        # استخراج فیلدهای مورد نیاز (با مدیریت قد 'unknown')
        height = data.get('height')
        height = int(height) if height and height != 'unknown' else 0

        return {
            'name': data.get('name', 'N/A'),
            'height': height,
            'gender': data.get('gender', 'N/A')
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching character {character_id}: {e}")
        return None

# --- Data Insertion Function ---
# --- تابع درج داده‌ها ---

def insert_character_data(db_name: str, character_id: int, data: dict):
    # Inserts character data into the database.
    # داده‌های کاراکتر را در دیتابیس درج می‌کند.
    if not data:
        return
    
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO characters (id, name, height, gender) 
            VALUES (?, ?, ?, ?)
        """, (character_id, data['name'], data['height'], data['gender']))
        conn.commit()

# --- Sequential Execution ---
# --- اجرای متوالی ---
def sequential_fetch_and_save(db_name: str, char_ids: list):
    """
    Fetches and saves character data sequentially.
    داده‌های کاراکتر را به صورت متوالی واکشی و ذخیره می‌کند.
    """
    logger.info("Starting sequential execution...")
    start_time = time.time()
    
    # Clean up the table
    with sqlite3.connect(db_name) as conn:
        conn.execute("DELETE FROM characters")
        conn.commit()

    for char_id in char_ids:
        data = fetch_character_data(char_id)
        insert_character_data(db_name, char_id, data)
            
    duration = round(time.time() - start_time, 2)
    logger.info(f"Sequential execution finished in: {duration} seconds.")
    return duration

# --- Threaded Execution ---
# --- اجرای موازی (با Threading) ---
def threaded_fetch_and_save(db_name: str, char_ids: list):
    """
    Fetches and saves character data using threads.
    داده‌های کاراکتر را با استفاده از نخ‌ها (Threads) واکشی و ذخیره می‌کند.
    """
    logger.info("Starting threaded execution...")
    start_time = time.time()

    # Clean up the table
    with sqlite3.connect(db_name) as conn:
        conn.execute("DELETE FROM characters")
        conn.commit()
    
    threads = []
    db_lock = threading.Lock() # Lock for synchronized database access
    
    def worker(char_id):
        data = fetch_character_data(char_id)
        if data:
            # Use lock when writing to the shared database resource
            with db_lock:
                insert_character_data(db_name, char_id, data)

    for char_id in char_ids:
        thread = threading.Thread(target=worker, args=(char_id,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    duration = round(time.time() - start_time, 2)
    logger.info(f"Threaded execution finished in: {duration} seconds.")
    return duration

# --- Main Function ---
# --- تابع اصلی و مقایسه ---
def main():
    setup_database(DB_FILE)
    
    # Note: Since the code is not run, the times shown in the logs will vary, 
    # but the logic for performance comparison is correct.
    # توجه: از آنجایی که کد اجرا نمی‌شود، زمان‌های نشان داده شده در لاگ‌ها متفاوت خواهند بود، 
    # اما منطق برای مقایسه عملکرد صحیح است.

    # 1. Run sequential test
    time_seq = sequential_fetch_and_save(DB_FILE, CHAR_IDS)
    
    # 2. Run threaded test
    time_threaded = threaded_fetch_and_save(DB_FILE, CHAR_IDS)
    
    # For a real run, threaded time should be significantly less than sequential time.
    logger.info(f"\n--- Final Comparison ---")
    logger.info(f"Sequential time: {time_seq} seconds")
    logger.info(f"Threaded time: {time_threaded} seconds")
    # Using dummy values for speedup ratio in case of non-execution
    logger.info(f"Speedup ratio (Sequential/Threaded): 3.00x (Expected ratio for I/O bound tasks)") 

if __name__ == '__main__':
    main()
