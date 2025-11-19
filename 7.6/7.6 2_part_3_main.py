# main.py - Task 2: OOP Configuration

import logging
import sys
from logging import StreamHandler, Formatter
from app import run_calculator

# --- پیکربندی شیءگرا برای لاگ‌گیری ---

def setup_oop_logging():
    """
    لاگ‌گیری را با استفاده از رویکرد برنامه‌نویسی شیءگرا (Logger, Handler, Formatter)
    تنظیم می‌کند تا لاگ‌ها با فرمت دلخواه به stdout ارسال شوند.
    """
    
    # 1. دریافت لاگر اصلی (Root Logger)
    root_logger = logging.getLogger()
    # سطح لاگر ریشه را روی DEBUG تنظیم می‌کنیم
    root_logger.setLevel(logging.DEBUG)  

    # 2. ایجاد قالب‌دهنده (Formatter)
    # فرمت مورد نیاز: سطح | لاگر | زمان | شماره خط | پیام
    # % (lineno)d برای شماره خط ضروری است
    log_format = '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s'
    formatter = Formatter(log_format)

    # 3. ایجاد مدیریت‌کننده (Handler) برای خروجی به stdout
    # StreamHandler(sys.stdout) تضمین می‌کند که خروجی به جریان استاندارد می‌رود
    console_handler = StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG) 
    
    # 4. متصل کردن Formatter به Handler
    console_handler.setFormatter(formatter)
    
    # 5. متصل کردن Handler به Logger
    root_logger.addHandler(console_handler)
    
    root_logger.info("پیکربندی لاگ‌گیری به روش شیءگرا با موفقیت انجام شد.")


# --- اجرای اصلی ---
if __name__ == '__main__':
    # 1. تنظیم محیط لاگ‌گیری
    setup_oop_logging()
    
    # 2. اجرای برنامه ماشین حساب
    run_calculator()
