#  Задача 2. Сложность пароля

import re # Import the regular expression module / ماژول عبارت منظم را وارد کنید
import os # Import os module to check file existence / ماژول os را برای بررسی وجود فایل وارد کنید
from typing import Set # Import Set for type hinting / Set را برای Type Hinting وارد کنید

# --- Configuration for word list ---
# --- پیکربندی برای لیست کلمات ---
# Path to the English word list file. Adjust this if your file is in a different location.
# مسیر فایل لیست کلمات انگلیسی. اگر فایل شما در مکان دیگری است، این را تنظیم کنید.
WORD_LIST_FILE = '/usr/share/dict/words'
# Fallback for systems that might not have the file at the standard path
# (e.g., if you download it to the current directory for testing on non-Linux).
# یک بازگشت برای سیستم‌هایی که ممکن است فایل را در مسیر استاندارد نداشته باشند
# (مثلاً اگر آن را در دایرکتوری فعلی برای آزمایش در سیستم‌های غیر لینوکس دانلود می‌کنید).
if not os.path.exists(WORD_LIST_FILE):
    # This assumes 'words' file might be in the same directory as the script.
    # If you downloaded a specific file name, adjust here.
    # این فرض می‌کند که فایل 'words' ممکن است در همان دایرکتوری اسکریپت باشد.
    # اگر یک نام فایل خاص را دانلود کرده‌اید، اینجا را تنظیم کنید.
    current_dir_word_file = os.path.join(os.path.dirname(__file__), 'words')
    if os.path.exists(current_dir_word_file):
        WORD_LIST_FILE = current_dir_word_file
    else:
        # If neither path works, print a warning. The set will be empty.
        # اگر هیچ یک از مسیرها کار نکرد، یک هشدار چاپ کنید. مجموعه خالی خواهد بود.
        print(f"WARNING: Word list file not found at '{WORD_LIST_FILE}' or '{current_dir_word_file}'. "
              "Password strength check for English words will not be fully functional.", file=sys.stderr)
        # You might want to raise an error or handle this more robustly in a real application.
        # ممکن است بخواهید یک خطا ایجاد کنید یا این را در یک برنامه واقعی به صورت قوی‌تر مدیریت کنید.

# --- Global set to store pre-processed English words ---
# --- مجموعه جهانی برای ذخیره کلمات انگلیسی پیش‌پردازش شده ---
_ENGLISH_WORDS: Set[str] = set()
_WORDS_LOADED = False

def _load_english_words():
    """
    Loads English words from a file into a global set.
    Words are converted to lowercase and only those longer than 4 characters are kept.
    This function should be called only once.
    
    کلمات انگلیسی را از یک فایل در یک مجموعه جهانی بارگذاری می‌کند.
    کلمات به حروف کوچک تبدیل می‌شوند و فقط کلمات طولانی‌تر از 4 کاراکتر نگهداری می‌شوند.
    این تابع باید فقط یک بار فراخوانی شود.
    """
    global _ENGLISH_WORDS, _WORDS_LOADED
    if _WORDS_LOADED:
        return

    print(f"Loading English words from {WORD_LIST_FILE}...", file=sys.stderr) # Logging for debugging / برای اشکال‌زدایی
    try:
        with open(WORD_LIST_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip().lower() # Remove whitespace and convert to lowercase / فضای خالی را حذف و به حروف کوچک تبدیل کنید
                if len(word) > 4 and word.isalpha(): # Check length and ensure it's purely alphabetic / طول را بررسی کنید و مطمئن شوید که کاملاً الفبایی است
                    _ENGLISH_WORDS.add(word)
        _WORDS_LOADED = True
        print(f"Loaded {_ENGLISH_WORDS.__len__()} English words.", file=sys.stderr) # Logging for debugging / برای اشکال‌زدایی
    except FileNotFoundError:
        print(f"Error: Word list file not found at '{WORD_LIST_FILE}'. Password strength check might be weak.", file=sys.stderr)
    except Exception as e:
        print(f"Error loading word list: {e}", file=sys.stderr)
    

def is_strong_password(password: str) -> bool:
    """
    Checks if a password is "strong" according to new security standards:
    it should not contain common English words longer than 4 characters.
    
    بررسی می‌کند که آیا رمز عبور طبق استانداردهای امنیتی جدید "قوی" است:
    نباید شامل کلمات انگلیسی رایج طولانی‌تر از 4 کاراکتر باشد.

    Args:
        password (str): The password string to check. / رشته رمز عبور برای بررسی.

    Returns:
        bool: True if the password is strong (does not contain disallowed English words),
              False otherwise.
              True اگر رمز عبور قوی باشد (کلمات انگلیسی غیرمجاز را شامل نمی‌شود)،
              در غیر این صورت False.
    """
    if not _WORDS_LOADED:
        _load_english_words() # Ensure words are loaded on first call / اطمینان حاصل کنید که کلمات در اولین فراخوانی بارگذاری شده‌اند

    if not _ENGLISH_WORDS:
        print("WARNING: English word list is empty. Password strength check for words is disabled.", file=sys.stderr)
        return True # If no word list, assume strong based on this criterion / اگر لیست کلمه ای وجود ندارد، بر اساس این معیار قوی فرض کنید

    # Use regular expression to find all alphabetic words in the password.
    # \b matches word boundaries, [a-zA-Z]+ matches one or more letters.
    # از عبارت منظم برای یافتن تمام کلمات الفبایی در رمز عبور استفاده کنید.
    # \b مرزهای کلمه را مطابقت می‌دهد، [a-zA-Z]+ یک یا چند حرف را مطابقت می‌دهد.
    words_in_password = re.findall(r'\b[a-zA-Z]+\b', password.lower())

    for word in words_in_password:
        if len(word) > 4 and word in _ENGLISH_WORDS:
            # Found a common English word longer than 4 characters in the password.
            # یک کلمه انگلیسی رایج طولانی‌تر از 4 کاراکتر در رمز عبور یافت شد.
            return False
            
    return True

# --- Example Usage (for testing this module directly) ---
if __name__ == '__main__':
    # Force load for direct testing / بارگذاری اجباری برای تست مستقیم
    _load_english_words()

    print(f"Is 'MyPassword123' strong? {is_strong_password('MyPassword123')}") # Expected: True (unless "mypassword" is in dict)
    print(f"Is 'password123' strong? {is_strong_password('password123')}") # Expected: False (if 'password' is in dict)
    print(f"Is 'SecretWord!@#' strong? {is_strong_password('SecretWord!@#')}") # Expected: False (if 'secretword' is in dict)
    print(f"Is 'short' strong? {is_strong_password('short')}") # Expected: True (length <= 4)
    print(f"Is 'lengthyword' strong? {is_strong_password('lengthyword')}") # Expected: False (if 'lengthyword' is in dict)
    print(f"Is 'ThisIsAStrongOne' strong? {is_strong_password('ThisIsAStrongOne')}") # Expected: False (if "this", "is", "strong", "one" are in dict, "is" and "one" are too short)
    print(f"Is 'FLaskApp' strong? {is_strong_password('FLaskApp')}") # Expected: False (if "flaskapp" is in dict)
    print(f"Is 'Рython_код' strong? {is_strong_password('Рython_код')}") # Expected: True (non-English characters or not in dict)
    print(f"Is 'unCOMMONword' strong? {is_strong_password('unCOMMONword')}") # Expected: True (if "uncommonword" is NOT in dict)
