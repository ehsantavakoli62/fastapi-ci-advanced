# main.py - Task 4: Implementing dictConfig

import logging.config
from app import run_calculator
from logging_config import dict_config # وارد کردن دیکشنری پیکربندی


def setup_dict_logging():
    """
    پیکربندی لاگ‌گیری را با استفاده از دیکشنری (dict-config) اعمال می‌کند.
    """
    # **توجه:** این خط، جایگزین کد قبلی (OOP یا basicConfig) می‌شود.
    logging.config.dictConfig(dict_config)
    logging.info("Dict logging configuration applied successfully.")


# --- اجرای اصلی ---
if __name__ == '__main__':
    # 1. تنظیم محیط لاگ‌گیری با استفاده از دیکشنری
    setup_dict_logging()
    
    # 2. اجرای برنامه ماشین حساب
    run_calculator()
