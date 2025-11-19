# app.py

import logging
from utils import add, subtract, multiply, divide

# Logger is created with the name of the module
# لاگر با نام ماژول ایجاد می‌شود
logger = logging.getLogger('app')

def run_calculator():
    """Runs the console calculator application."""
    
    logger.info("Calculator application started.")

    try:
        # Input processing and logging (INFO level)
        num1 = float(input("Enter first number: "))
        logger.info(f"First number entered: {num1}")
        
        num2 = float(input("Enter second number: "))
        logger.info(f"Second number entered: {num2}")
        
        op = input("Enter operation (+, -, *, /): ")
        logger.info(f"Operation selected: {op}")
        
    except ValueError:
        # Log error at WARNING level for improper input
        logger.warning("Invalid input detected. Please enter valid numbers.")
        return

    # Perform calculation based on the selected operation
    if op == '+':
        result = add(num1, num2)
    elif op == '-':
        result = subtract(num1, num2)
    elif op == '*':
        result = multiply(num1, num2)
    elif op == '/':
        result = divide(num1, num2)
    else:
        # Log warning for unknown operation
        logger.warning(f"Unknown operation selected: {op}")
        result = "Error: Invalid operation"

    # Print the final result (this is the desired output for the user)
    print(f"Result: {result}")
    logger.info("Calculator application finished.")

if __name__ == '__main__':
    # When running app.py directly, we need a basic configuration (temporary)
    # هنگام اجرای مستقیم app.py، به یک پیکربندی اولیه نیاز داریم (موقت)
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    run_calculator()
