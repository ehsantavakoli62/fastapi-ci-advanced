# main.py 

import logging.config
import logging_tree
from app import run_calculator
from logging_config import dict_config 
import sys # Import sys for redirection / وارد کردن sys برای تغییر مسیر خروجی


def setup_and_display_tree():
    """
    Applies the dictionary configuration and prints the logger tree to a file.
    پیکربندی دیکشنری را اعمال کرده و سپس درخت لاگرها را در یک فایل چاپ می‌کند.
    """
    # 1. Apply logging configuration
    # اعمال پیکربندی لاگ‌گیری
    logging.config.dictConfig(dict_config)
    logging.info("Dict logging configuration applied.")

    # 2. Ensure loggers are initialized by calling app function
    # اطمینان از مقداردهی اولیه لاگرها
    run_calculator() 
    
    # 3. Print the logger tree structure to the console (optional but helpful)
    # چاپ ساختار درخت لاگرها در کنسول (اختیاری)
    print("\n--- Logger Tree Structure (Console Output) ---")
    logging_tree.printout()
    print("---------------------------------------------")

    # 4. Redirect the tree output to the required file (logging_tree.txt)
    # هدایت خروجی درخت به فایل مورد نیاز (logging_tree.txt)
    output_filename = 'logging_tree.txt'
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        # Save the current stdout / ذخیره stdout فعلی
        original_stdout = sys.stdout
        # Redirect stdout to the file / هدایت stdout به فایل
        sys.stdout = f
        
        # Print the logger tree structure to the file
        # چاپ ساختار درخت لاگرها به فایل
        logging_tree.printout()
        
        # Restore the original stdout / بازگرداندن stdout اصلی
        sys.stdout = original_stdout
    
    print(f"\nLogger tree structure successfully written to {output_filename}")
    
    # Create another logger just for testing the tree structure definition
    # ایجاد یک لاگر دیگر برای تست تعریف ساختار درخت
    logging.getLogger('app.submodule').warning("A submodule logger is active.")


# --- اجرای اصلی ---
if __name__ == '__main__':
    setup_and_display_tree()
