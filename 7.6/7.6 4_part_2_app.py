# app.py - Task 4 (Standalone)

import logging
from utils import add, subtract, multiply, divide

# لاگر با نام ماژول ایجاد می‌شود
logger = logging.getLogger('app')

def run_calculator():
    """Runs the console calculator application."""
    
    logger.info("Calculator application started.")

    try:
        # ورودی‌ها
        num1 = float(input("Enter first number: "))
        logger.info(f"First number entered: {num1}")
        
        num2 = float(input("Enter second number: "))
        logger.info(f"Second number entered: {num2}")
        
        op = input("Enter operation (+, -, *, /): ")
        logger.info(f"Operation selected: {op}")
        
    except ValueError:
        # ثبت خطا با سطح WARNING برای ورودی نامناسب
        logger.warning("Invalid input detected. Please enter valid numbers.")
        return

    # انجام محاسبات
    if op == '+':
        result = add(num1, num2)
    elif op == '-':
        result = subtract(num1, num2)
    elif op == '*':
        result = multiply(num1, num2)
    elif op == '/':
        result = divide(num1, num2)
    else:
        # ثبت خطا با سطح WARNING برای عملیات نامشخص
        logger.warning(f"Unknown operation selected: {op}")
        result = "Error: Invalid operation"

    # نمایش نتیجه نهایی به کاربر
    print(f"Result: {result}")
    logger.info("Calculator application finished.")
