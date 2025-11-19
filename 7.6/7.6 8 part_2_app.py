# app.py 



import logging
from utils import add, divide

# Logger is created with the name of the module
# لاگر با نام ماژول ایجاد می‌شود
logger = logging.getLogger('app')

def run_calculator():
    """Runs the console calculator application and generates logs."""
    
    logger.info("Calculator service started.")
    
    # Generate some logs for both app and utils loggers
    # تولید چند لاگ برای تست لاگرهای app و utils
    
    # 1. Log from 'app' logger (INFO level)
    logger.info("User interaction session begins.") 
    
    # 2. Log from 'utils' logger (INFO level)
    add(10, 5) 
    
    # 3. Log an ERROR from 'utils' logger
    divide(10, 0)
    
    # 4. Log from 'app' logger (WARNING level)
    logger.warning("Session concluded successfully.")
