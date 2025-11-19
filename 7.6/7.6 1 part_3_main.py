# main.py

import logging
from app import run_calculator

# --- Basic Configuration for Logging ---
# پیکربندی اولیه برای لاگ‌گیری ---

# Set the overall logging level to DEBUG so we see all messages
# سطح کلی لاگ‌گیری را روی DEBUG تنظیم می‌کنیم تا همه پیام‌ها را ببینیم
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Execute the main application function
# اجرای تابع اصلی برنامه
if __name__ == '__main__':
    run_calculator()
