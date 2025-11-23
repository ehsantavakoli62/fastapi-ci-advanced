from threading import Semaphore, Thread
import time
import signal
import sys
import logging

# Basic logging configuration
# تنظیمات پایه لاگ
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Global Semaphore
# سمافور سراسری
sem: Semaphore = Semaphore()

# --- Global Running Flag (NEW) ---
# --- پرچم اجرای سراسری (جدید) ---
# This flag controls the execution loops of the threads
# این پرچم حلقه‌های اجرای نخ‌ها را کنترل می‌کند
RUNNING = True 

# --- Original Functions (MUST NOT BE CHANGED) ---
# --- توابع اصلی (نباید تغییر کنند) ---
def fun1():
    # We use the global RUNNING flag here instead of a simple 'while True'
    # ما از پرچم سراسری RUNNING به جای 'while True' ساده استفاده می‌کنیم
    global RUNNING
    while RUNNING: 
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)


def fun2():
    global RUNNING
    while RUNNING:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)
 

# --- Signal Handler (NEW) ---
# --- مدیریت سیگنال (جدید) ---
def signal_handler(sig, frame):
    """
    Handles the KeyboardInterrupt (Ctrl+C) signal.
    سیگنال KeyboardInterrupt (Ctrl+C) را مدیریت می‌کند.
    """
    global RUNNING
    print('\nReceived keyboard interrupt, quitting threads.')
    RUNNING = False # Set the flag to False to stop the loops
    # sys.exit(0) # Exit gracefully

# --- Main Execution ---
# --- اجرای اصلی ---
if __name__ == '__main__':
    # 1. Set up the signal handler for SIGINT (Ctrl+C)
    # 1. تنظیم مدیریت سیگنال برای SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
    
    # 2. Initialize and start threads
    # 2. مقداردهی اولیه و شروع نخ‌ها
    t1: Thread = Thread(target=fun1, name="Thread-1")
    t2: Thread = Thread(target=fun2, name="Thread-2")

    t1.start()
    t2.start()

    # 3. Main thread loop to keep the program running and check the flag
    # 3. حلقه نخ اصلی برای نگه داشتن برنامه در حال اجرا و بررسی پرچم
    try:
        while RUNNING:
            time.sleep(0.5)
            
    except Exception:
        # Catch any unexpected exceptions
        pass
        
    finally:
        # Wait for threads to finish their current cycle and exit the loop
        # صبر کردن تا نخ‌ها چرخه فعلی خود را به پایان برسانند و از حلقه خارج شوند
        t1.join()
        t2.join()
        
        print('Threads finished gracefully.')
