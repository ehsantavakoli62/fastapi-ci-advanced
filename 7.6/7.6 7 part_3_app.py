# app.py 
import logging
from utils import add, subtract, multiply, divide

# Logger is created with the name of the module
# لاگر با نام ماژول ایجاد می‌شود
logger = logging.getLogger('app')

def run_calculator():
    """Runs the console calculator application."""
    
    logger.info("Calculator application started (Task 7).") # This is ASCII

    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        op = input("Enter operation (+, -, *, /): ")
    except ValueError:
        logger.warning("Invalid input detected. Please enter valid numbers.")
        return

    # Call a function that produces a non-ASCII log message
    # فراخوانی تابعی که یک پیام لاگ غیر-ASCII تولید می‌کند
    result = subtract(num1, num2) 

    # Another non-ASCII log for testing the filter on 'app' logger
    # یک لاگ غیر-ASCII دیگر برای تست فیلتر روی لاگر 'app'
    logger.warning("Calculation finished. 🚀 Non-ASCII test.") 

    print(f"Result: {result}")
    logger.info("Calculator application finished.") # This is ASCII
