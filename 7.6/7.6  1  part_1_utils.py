# utils.py

import logging

# Logger is created with the name of the module
# لاگر با نام ماژول ایجاد می‌شود
logger = logging.getLogger('utils')


def add(x, y):
    """Adds two numbers and logs the operation."""
    # Log inputs at DEBUG level
    logger.debug(f"Adding numbers: {x} and {y}")
    result = x + y
    # Log result at INFO level
    logger.info(f"Addition result: {result}")
    return result

def subtract(x, y):
    """Subtracts two numbers and logs the operation."""
    logger.debug(f"Subtracting numbers: {x} from {y}")
    result = x - y
    logger.info(f"Subtraction result: {result}")
    return result

def multiply(x, y):
    """Multiplies two numbers and logs the operation."""
    logger.debug(f"Multiplying numbers: {x} and {y}")
    result = x * y
    logger.info(f"Multiplication result: {result}")
    return result

def divide(x, y):
    """Divides two numbers and logs the operation."""
    logger.debug(f"Dividing numbers: {x} by {y}")
    try:
        result = x / y
        logger.info(f"Division result: {result}")
        return result
    except ZeroDivisionError:
        # Log error at ERROR level
        logger.error("Error: Attempted to divide by zero!")
        return "Error: Division by zero"
