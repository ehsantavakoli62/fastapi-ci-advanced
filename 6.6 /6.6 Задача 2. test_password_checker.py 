import pytest
import os
import sys
from typing import Set

# It's better to import the module and access its attributes for mocking,
# rather than importing global variables directly if they are modified.
import password_checker 

# Use a fixture to capture stderr output / از یک فیچر برای گرفتن خروجی stderr استفاده کنید
@pytest.fixture
def capsys_without_autouse(capsys):
    """Provides capsys without autouse for specific warning checks."""
    """capsys را بدون autouse برای بررسی‌های هشدار خاص فراهم می‌کند."""
    return capsys

# Fixture to ensure words are loaded before tests, and to manage global state.
# We explicitly call _load_english_words to control when it happens.
@pytest.fixture(autouse=True)
def setup_word_list_for_tests():
    """
    Manages the global state of the word list (_ENGLISH_WORDS and _WORDS_LOADED)
    before and after each test to ensure a clean slate and proper loading.
    """
    # Save original state / حالت اصلی را ذخیره کنید
    original_words = set(password_checker._ENGLISH_WORDS)
    original_loaded_status = password_checker._WORDS_LOADED

    # Reset global state for the test / حالت جهانی را برای تست بازنشانی کنید
    password_checker._ENGLISH_WORDS.clear()
    password_checker._WORDS_LOADED = False
    
    # Load words for general tests, unless a test specifically mocks it / کلمات را برای تست‌های عمومی بارگذاری کنید، مگر اینکه تستی آن را Mock کند
    # Ensure this doesn't print warnings during normal test runs / اطمینان حاصل کنید که این در طول اجرای تست عادی هشداری چاپ نمی‌کند
    with open(os.devnull, 'w') as f:
        old_stderr = sys.stderr
        sys.stderr = f
        try:
            password_checker._load_english_words()
        finally:
            sys.stderr = old_stderr

    yield # Run the test / تست را اجرا کنید

    # Restore original state after test / حالت اصلی را پس از تست بازیابی کنید
    password_checker._ENGLISH_WORDS.clear()
    password_checker._ENGLISH_WORDS.update(original_words)
    password_checker._WORDS_LOADED = original_loaded_status


@pytest.fixture
def mock_word_list(monkeypatch):
    """
    Mocks the global _ENGLISH_WORDS set for specific test scenarios
    to avoid dependency on the actual file and provide controlled test data.
    """
    original_words = set(password_checker._ENGLISH_WORDS)
    original_loaded_status = password_checker._WORDS_LOADED
    
    password_checker._ENGLISH_WORDS.clear()
    password_checker._WORDS_LOADED = False

    def _set_mock_words(words_to_mock: Set[str]):
        password_checker._ENGLISH_WORDS.update(words_to_mock)
        password_checker._WORDS_LOADED = True
    
    yield _set_mock_words

    password_checker._ENGLISH_WORDS.clear()
    password_checker._ENGLISH_WORDS.update(original_words)
    password_checker._WORDS_LOADED = original_loaded_status


def test_strong_password_no_english_words(mock_word_list):
    """
    Test case: Password contains no English words from the disallowed list.
    """
    mock_word_list({"apple", "banana", "orange", "grape", "melon"}) 
    assert password_checker.is_strong_password("MyS3cur3P@ssw0rd") is True
    assert password_checker.is_strong_password("nonenglishword_123") is True 

def test_weak_password_contains_english_word(mock_word_list):
    """
    Test case: Password contains an English word from the disallowed list (case-insensitive).
    """
    mock_word_list({"password", "secret", "qwert"})
    assert password_checker.is_strong_password("MyPassword123") is False 
    assert password_checker.is_strong_password("secret_sauce") is False 
    assert password_checker.is_strong_password("AnotherSECRETword") is False 
    assert password_checker.is_strong_password("qwert123") is False

def test_weak_password_contains_multi_word_phrase(mock_word_list):
    """
    Test case: Password contains multiple English words (case-insensitive).
    """
    mock_word_list({"strong", "password", "secure"})
    assert password_checker.is_strong_password("ThisIsAStrongPassword") is False 
    assert password_checker.is_strong_password("BestSECUREPassWordEver") is False

def test_word_length_four_or_less_ignored(mock_word_list):
    """
    Test case: English words with length 4 or less should be ignored.
    """
    mock_word_list({"test", "data", "wordy", "longword"}) 
    assert password_checker.is_strong_password("MyTest123") is True 
    assert password_checker.is_strong_password("SomeDATAhere") is True 
    assert password_checker.is_strong_password("ThisIsAWordyPassword") is False 
    assert password_checker.is_strong_password("ThisIsALongword") is False

def test_non_alphabetic_characters_in_password_split_words(mock_word_list):
    """
    Test case: Non-alphabetic characters should correctly split words,
    and only full, valid English words should be checked.
    """
    mock_word_list({"super", "secret", "password", "secure"})
    assert password_checker.is_strong_password("Sup3rP@ssword") is False # 'password' should be found / 'password' باید پیدا شود
    assert password_checker.is_strong_password("S-U-P-E-R") is True # 'super' is split, 's', 'u', 'p', 'e', 'r' are too short / 'super' تقسیم شده، 's', 'u', 'p', 'e', 'r' خیلی کوتاه هستند
    assert password_checker.is_strong_password("My$ecureP@ssword") is False 
    assert password_checker.is_strong_password("My_Awesome_Password_123") is False # 'awesome' and 'password' should be found / 'awesome' و 'password' باید پیدا شوند

def test_empty_password_is_strong():
    """
    Test case: An empty password should be considered strong (as it contains no words).
    """
    assert password_checker.is_strong_password("") is True

def test_password_with_only_numbers_or_symbols_is_strong():
    """
    Test case: Password containing only numbers or symbols should be considered strong.
    """
    assert password_checker.is_strong_password("1234567890") is True
    assert password_checker.is_strong_password("!@#$%^&*()") is True
    assert password_checker.is_strong_password("!P@ssw0rd!123") is True # No English word found / هیچ کلمه انگلیسی یافت نشد

def test_no_word_list_file_returns_true(monkeypatch, capsys_without_autouse):
    """
    Test case: If the word list file does not exist, the check should return True
    and a warning should be printed to stderr.
    """
    # Temporarily set WORD_LIST_FILE to a non-existent path / موقتاً WORD_LIST_FILE را به یک مسیر ناموجود تنظیم کنید
    monkeypatch.setattr(password_checker, 'WORD_LIST_FILE', '/non/existent/path/to/words.txt')
    
    # Clear and reset the loaded status to force reload / وضعیت بارگذاری شده را پاک و بازنشانی کنید تا بارگذاری مجدد اجباری شود
    password_checker._ENGLISH_WORDS.clear()
    password_checker._WORDS_LOADED = False
    
    # The check should return True because no words can be loaded / بررسی باید True برگرداند زیرا هیچ کلمه‌ای نمی‌تواند بارگذاری شود
    assert password_checker.is_strong_password("AnyPasswordWillBeStrong") is True
    
    # Capture stderr and check for the warning message / stderr را بگیرید و پیام هشدار را بررسی کنید
    captured = capsys_without_autouse.readouterr()
    assert "WARNING: Word list file not found" in captured.err

def test_word_list_loading_error_returns_true(monkeypatch, capsys_without_autouse):
    """
    Test case: If there's an error loading the word list (e.g., permission issue),
    the check should return True and an error should be printed to stderr.
    """
    # Mock open to raise an OSError / open را Mock کنید تا یک OSError ایجاد کند
    def mock_open(*args, **kwargs):
        raise OSError("Permission denied for word list file")
    
    monkeypatch.setattr('builtins.open', mock_open)
    monkeypatch.setattr(password_checker, 'WORD_LIST_FILE', '/dummy/existing/path.txt') # Set a dummy path / یک مسیر ساختگی تنظیم کنید

    password_checker._ENGLISH_WORDS.clear()
    password_checker._WORDS_LOADED = False

    assert password_checker.is_strong_password("AnyPasswordWillBeStrong") is True
    
    captured = capsys_without_autouse.readouterr()
    assert "Error loading word list: Permission denied" in captured.err

def test_long_password_without_dictionary_words():
    """
    Test case: A long, complex password without dictionary words.
    """
    # This test will use the actual loaded word list.
    # If the word list is empty (e.g., file not found), it will pass.
    # If it's loaded, it will check against actual words.
    password = "Th1s!s@Sup3rDuP3rS3cr3tP@ssw0rdW!thN0D!ct!onAryW0rds"
    assert password_checker.is_strong_password(password) is True

def test_password_containing_short_word_and_long_non_word(mock_word_list):
    """
    Test case: Password contains a short English word (ignored) and a long non-English-dictionary-word.
    """
    mock_word_list({"longword"}) # Only 'longword' is in the dictionary / فقط 'longword' در دیکشنری است
    assert password_checker.is_strong_password("test_verylongnonword_longword") is False # 'longword' is found / 'longword' یافت شد
    assert password_checker.is_strong_password("test_verylongnonword") is True # 'test' is short, 'verylongnonword' not in dictionary / 'test' کوتاه، 'verylongnonword' در دیکشنری نیست
