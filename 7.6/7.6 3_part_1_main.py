# main.py 

import logging
import sys
from logging import StreamHandler, Formatter, FileHandler
from app import run_calculator

# --- پیکربندی لاگ‌گیری ---

def setup_oop_logging():
    """
    لاگ‌گیری را با رویکرد OOP تنظیم می‌کند و دو مدیریت‌کننده فایل (برای DEBUG و ERROR)
    و یک مدیریت‌کننده کنسول را اضافه می‌کند.
    """
    
    # 1. دریافت لاگر اصلی (Root Logger) و تنظیم سطح
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  

    # 2. ایجاد قالب‌دهنده (Formatter) - همان قالب وظیفه ۲
    log_format = '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s'
    formatter = Formatter(log_format)

    # --- 3. مدیریت‌کننده‌های فایل (File Handlers) ---
    
    # الف) مدیریت‌کننده برای لاگ‌های سطح DEBUG و بالاتر (مثلاً در calc_debug.log)
    # سطح FileHandler را روی DEBUG تنظیم می‌کنیم
    debug_file_handler = FileHandler('calc_debug.log', encoding='utf-8')
    debug_file_handler.setLevel(logging.DEBUG) 
    debug_file_handler.setFormatter(formatter)
    
    # ب) مدیریت‌کننده برای لاگ‌های سطح ERROR و بالاتر (مثلاً در calc_error.log)
    # سطح FileHandler را روی ERROR تنظیم می‌کنیم
    error_file_handler = FileHandler('calc_error.log', encoding='utf-8')
    error_file_handler.setLevel(logging.ERROR) 
    error_file_handler.setFormatter(formatter)
    
    # --- 4. مدیریت‌کننده کنسول (Stream Handler) - از وظیفه ۲ ---
    
    # مدیریت‌کننده خروجی به stdout (کنسول)
    console_handler = StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO) # مثلاً فقط INFO و بالاتر در کنسول نمایش داده شود
    console_handler.setFormatter(formatter)
    
    # 5. متصل کردن Handlerها به Logger
    root_logger.addHandler(debug_file_handler)
    root_logger.addHandler(error_file_handler)
    root_logger.addHandler(console_handler)
    
    root_logger.info("پیکربندی چند سطحی لاگ‌گیری با موفقیت انجام شد.")


# --- اجرای اصلی ---
if __name__ == '__main__':
    setup_oop_logging()
    # اجرای برنامه ماشین حساب
    run_calculator()
