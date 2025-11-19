# app.py 
import logging
from utils import add, subtract, multiply, divide

# لاگر با نام ماژول ایجاد می‌شود
logger = logging.getLogger('app') # این لاگر نباید در utils.log ثبت شود

def run_calculator():
    """Runs the console calculator application."""
    
    logger.info("Calculator application started.")

    try:
        num1 = float(input("Enter first number: "))
        logger.info(f"First number entered: {num1}")
        
        num2 = float(input("Enter second number: "))
        logger.info(f"Second number entered: {num2}")
        
        op = input("Enter operation (+, -, *, /): ")
        logger.info(f"Operation selected: {op}")
        
    except ValueError:
        logger.warning("Invalid input detected. Please enter valid numbers.")
        return

    if op == '+':
        result = add(num1, num2)
    elif op == '-':
        result = subtract(num1, num2)
    elif op == '*':
        result = multiply(num1, num2)
    elif op == '/':
        result = divide(num1, num2)
    else:
        logger.warning(f"Unknown operation selected: {op}")
        result = "Error: Invalid operation"

    print(f"Result: {result}")
    logger.info("Calculator application finished.")
