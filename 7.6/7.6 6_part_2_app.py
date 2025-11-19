# app.py 

import logging
from utils import add, subtract, multiply, divide # Imports are needed to fully define the structure

# Logger is created with the name of the module
# لاگر با نام ماژول ایجاد می‌شود
logger = logging.getLogger('app')

def run_calculator():
    """Runs the console calculator application. / برنامه ماشین حساب کنسولی را اجرا می‌کند."""
    
    # Just defining the function, no need to run the full calculator input for this task
    logger.info("Calculator application setup complete (Task 6).")
    # We call a utility function to ensure both loggers are active
    # فراخوانی یک تابع کمکی برای اطمینان از فعال بودن هر دو لاگر
    add(1, 1)
