# utils.py
import logging

# Logger is created with the name of the module
# لاگر با نام ماژول ایجاد می‌شود
logger = logging.getLogger('utils')


def add(x, y):
    """Adds two numbers and logs the operation."""
    logger.debug(f"Adding numbers: {x} and {y}")
    result = x + y
    logger.info(f"Addition result: {result}")
    return result

def subtract(x, y):
    """Subtracts two numbers and logs the operation."""
    logger.debug(f"Subtracting numbers: {x} from {y}")
    result = x - y
    # This log contains non-ASCII characters and should be filtered out
    # این لاگ حاوی کاراکترهای غیر-ASCII است و باید فیلتر شود
    logger.info(f"Subtraction result with non-ASCII: {result}  ÎŒØ∏‡°⁄·°€") 
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
        logger.error("Error: Attempted to divide by zero! This is ASCII.")
        return "Error: Division by zero"
