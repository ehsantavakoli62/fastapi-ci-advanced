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

# --- Database Setup ---
# --- تنظیم دیتابیس ---

def setup_database(db_name: str):
    # Initializes the SQLite database and creates the table if it doesn't exist.
    # دیتابیس SQLite را مقداردهی اولیه می‌کند و جدول را در صورت عدم وجود ایجاد می‌کند.
    
    # We use a context manager for connection.
    # از context manager برای اتصال استفاده می‌کنیم.
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        # Creating the table: name, height, gender
        # ایجاد جدول: نام، قد، جنسیت
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
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        
        # Extract required fields and convert height to integer (using 'unknown' if missing)
        # استخراج فیلدهای مورد نیاز و تبدیل قد به عدد صحیح
        height = data.get('height')
        if height and height != 'unknown':
            height = int(height)
        else:
            height = 0 # Use 0 if height is unknown or missing

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
