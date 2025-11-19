# main.py 

import logging.config
import logging
from app import run_app
from utils import example_func
import sys
import json

# --- 1. DictConfig Equivalent (As determined from INI file) ---
dict_config = {
    'version': 1,
    'disable_existing_loggers': False, 
    'formatters': {
        'simpleFormatter': {
            'format': '%(levelname)s: %(name)s: %(message)s',
            'datefmt': None,
        },
        'detailedFormatter': {
            'format': '%(asctime)s | %(levelname)s | %(name)s | %(lineno)d | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'consoleHandler': {
            'class': 'logging.StreamHandler', 
            'level': 'DEBUG',
            'formatter': 'simpleFormatter',
            'stream': 'ext://sys.stdout', 
        },
        'fileHandler': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'detailedFormatter',
            'filename': 'app.log',
            'mode': 'w',
        }
    },
    'loggers': {
        'app': {
            'level': 'INFO',
            'handlers': ['consoleHandler', 'fileHandler'],
            'propagate': False,
        },
        'utils': {
            'level': 'DEBUG',
            'handlers': ['consoleHandler'],
            'propagate': False,
        }
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['consoleHandler'],
    }
}

# --- 2. Execution ---

def setup_logging():
    """
    Applies the dictionary configuration, which is the equivalent of the INI file.
    پیکربندی دیکشنری را که معادل فایل INI است، اعمال می‌کند.
    """
    logging.config.dictConfig(dict_config)
    logging.info("Dict configuration (INI equivalent) applied successfully.")

if __name__ == '__main__':
    # Print the equivalent dictionary for submission assessment
    # چاپ دیکشنری معادل برای ارزیابی تحویل
    print("--- INI Equivalent DictConfig (for submission) ---")
    print(json.dumps(dict_config, indent=4))
    print("--------------------------------------------------\n")
    
    # Apply and run the application to demonstrate functionality
    # اعمال و اجرای برنامه برای نمایش عملکرد
    setup_logging()
    
    print("Running application (Check console and app.log for output):")
    run_app()
    example_func()
