import re # Import the regular expression module
import os # Import os module to check file existence
from typing import Set # Import Set for type hinting

# --- Configuration for word list ---
WORD_LIST_FILE = '/usr/share/dict/words'
# Fallback to check in the script's directory
if not os.path.exists(WORD_LIST_FILE):
    current_dir_word_file = os.path.join(os.path.dirname(__file__), 'words')
    if os.path.exists(current_dir_word_file):
        WORD_LIST_FILE = current_dir_word_file
    # If neither path works, WORD_LIST_FILE remains the original non-existent path.
    # The _load_english_words function will handle the FileNotFoundError gracefully.

# --- Global set to store pre-processed English words ---
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

    try:
        with open(WORD_LIST_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip().lower()
                if len(word) > 4 and word.isalpha():
                    _ENGLISH_WORDS.add(word)
        _WORDS_LOADED = True
    except FileNotFoundError:
        # If the file is not found, _ENGLISH_WORDS will remain empty,
        # and _WORDS_LOADED will still be set to True to prevent repeated attempts.
        _WORDS_LOADED = True
    except Exception:
        # Catch any other potential errors during file reading
        # and ensure _WORDS_LOADED is set to True to prevent repeated attempts.
        _WORDS_LOADED = True
    

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
        _load_english_words()

    if not _ENGLISH_WORDS:
        # If word list failed to load or is empty, bypass this specific check.
        # This implies passwords are "strong" from the perspective of English words.
        return True 

    # Use regular expression to find all alphabetic words in the password.
    # \b matches word boundaries, [a-zA-Z]+ matches one or more letters.
    words_in_password = re.findall(r'\b[a-zA-Z]+\b', password.lower())

    for word in words_in_password:
        if len(word) > 4 and word in _ENGLISH_WORDS:
            return False
            
    return True
