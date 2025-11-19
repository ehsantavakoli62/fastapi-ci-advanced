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
# Other utility functions remain similar
