# utils.py 


import logging

# Logger is created with the name of the module
# لاگر با نام ماژول ایجاد می‌شود
logger = logging.getLogger('utils')


def add(x, y):
    """Adds two numbers and logs the operation. / دو عدد را جمع کرده و عملیات را لاگ می‌کند."""
    logger.debug(f"Adding numbers: {x} and {y}")
    result = x + y
    logger.info(f"Addition result: {result}")
    return result

def divide(x, y):
    """Divides two numbers and logs the operation. / دو عدد را تقسیم کرده و عملیات را لاگ می‌کند."""
    try:
        result = x / y
        logger.info(f"Division result: {result}")
        return result
    except ZeroDivisionError:
        # ثبت خطا با سطح ERROR
        logger.error("Error: Attempted to divide by zero!")
        return "Error: Division by zero"
