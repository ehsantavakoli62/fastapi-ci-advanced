# main.py 


import logging.config
from app import run_calculator
from logging_config import dict_config 


def setup_dict_logging():
    """
    Applies the dictionary configuration, including the custom ASCII filter.
    پیکربندی دیکشنری، شامل فیلتر سفارشی ASCII را اعمال می‌کند.
    """
    # Apply configuration
    # اعمال پیکربندی
    logging.config.dictConfig(dict_config)
    logging.info("Dict logging configuration with ASCII Filter applied successfully.")


# --- اجرای اصلی ---
if __name__ == '__main__':
    # 1. تنظیم محیط لاگ‌گیری
    setup_dict_logging()
    
    # 2. اجرای برنامه ماشین حساب
    run_calculator()
