# main.py 


import logging.config
import logging
import threading
from app import run_calculator
import time

# --- DICT CONFIGURATION (Client Side) ---
# پیکربندی دیکشنری سمت کلاینت (ماشین حساب)
dict_config = {
    'version': 1,
    'disable_existing_loggers': False, 

    # 1. Formatters / قالب‌دهنده‌ها
    'formatters': {
        'default_formatter': {
            'format': '%(levelname)s | %(name)s | %(asctime)s | %(message)s'
        },
    },

    # 2. Handlers / مدیریت‌کننده‌ها
    'handlers': {
        # HTTPHandler to send logs to the Flask server
        # HTTPHandler برای ارسال لاگ‌ها به سرور Flask
        'http_handler': {
            'class': 'logging.handlers.HTTPHandler',
            'host': '127.0.0.1:3000', # The address where the server is running
            'url': '/log',
            'method': 'POST',
            'formatter': 'default_formatter',
            'level': 'INFO', # Only send INFO and above to the server
        },
        # Console handler for local visibility (optional)
        # هندلر کنسول برای نمایش محلی (اختیاری)
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
            'level': 'DEBUG', 
        }
    },

    # 3. Loggers / لاگرها
    'loggers': {
        'app': {
            'level': 'DEBUG',
            'handlers': ['http_handler', 'console_handler'], # Send to server and console
            'propagate': False,
        },
        'utils': {
            'level': 'DEBUG',
            'handlers': ['http_handler', 'console_handler'], # Send to server and console
            'propagate': False,
        },
        # Filter out verbose logs from external libraries like urllib (used by HTTPHandler)
        # فیلتر کردن لاگ‌های پر سر و صدای کتابخانه‌های خارجی مانند urllib
        'urllib3': { 
            'level': 'WARNING',
            'propagate': False,
        }
    },

    # 4. Root Logger / لاگر ریشه
    'root': {
        'level': 'WARNING',
        'handlers': ['console_handler'],
    }
}


def setup_dict_logging():
    """
    Applies the dictionary configuration, including HTTPHandler.
    پیکربندی دیکشنری شامل HTTPHandler را اعمال می‌کند.
    """
    logging.config.dictConfig(dict_config)
    logging.info("Client logging setup complete.")

# --- Execution ---

def run_client():
    """
    Sets up logging and runs the calculator service.
    لاگ‌گیری را تنظیم کرده و سرویس ماشین حساب را اجرا می‌کند.
    """
    setup_dict_logging()
    # Wait a moment for the server to fully start
    # یک لحظه صبر می‌کنیم تا سرور کاملاً راه‌اندازی شود
    time.sleep(1) 
    run_calculator()
    

if __name__ == '__main__':
    # You need to run the server (log_server.py) in one terminal 
    # and the client (main.py) in a separate terminal.
    
    # 1. Start the server in a separate thread for demonstration (Only for simple demo)
    # اگر می‌خواهید هر دو را در یک اسکریپت اجرا کنید، از threading استفاده کنید.
    # توصیه می‌شود سرور را در یک ترمینال جداگانه اجرا کنید: python log_server.py
    
    print("--- WARNING: Server must be run in a separate terminal via 'python log_server.py' ---")
    print("Attempting to run client (main.py) now...")
    
    run_client()
