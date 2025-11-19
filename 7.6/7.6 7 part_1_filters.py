# filters.py

import logging
# The LogRecord object contains all information about the log message
# شیء LogRecord شامل تمام اطلاعات مربوط به پیام لاگ است

class AsciiFilter(logging.Filter):
    """
    A custom filter that accepts log records only if their message 
    contains exclusively ASCII characters.
    یک فیلتر سفارشی که تنها در صورتی رکورد لاگ را می‌پذیرد که پیام آن 
    منحصراً حاوی کاراکترهای ASCII باشد.
    """
    def filter(self, record):
        # The actual log message is stored in record.getMessage() or record.msg
        # پیام واقعی لاگ در record.getMessage() یا record.msg ذخیره می‌شود
        log_message = record.getMessage()
        
        # Check if the message contains only ASCII characters using the built-in method
        # بررسی اینکه آیا پیام تنها شامل کاراکترهای ASCII است با استفاده از متد داخلی
        is_ascii = log_message.isascii()
        
        # Returns True if the message should be processed (i.e., it is ASCII)
        # اگر پیام باید پردازش شود (یعنی ASCII است)، True برمی‌گرداند
        return is_ascii
