import threading
import time
import requests
import queue
import logging

# Basic logging configuration
# تنظیمات پایه لاگ
logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')
logger = logging.getLogger(__name__)

# Constants
# ثابت‌ها
NUM_THREADS = 10
LOG_DURATION = 20 # seconds
LOG_FILE = 'sorted_logs.txt'
SERVER_URL = "http://127.0.0.1:8080/timestamp/"

# Queue to store logs unsorted
# صف برای ذخیره لاگ‌های نامرتب
log_queue = queue.Queue()

# --- Worker Thread ---
# --- نخ کارگر ---
class LogWorker(threading.Thread):
    
    def run(self):
        start_time = time.time()
        
        while time.time() - start_time < LOG_DURATION:
            # 1. Get current timestamp (client-side)
            # 1. گرفتن timestamp فعلی (سمت کلاینت)
            current_ts = int(time.time()) 
            
            # 2. Make request to get formatted date from server
            # 2. ارسال درخواست برای گرفتن تاریخ فرمت شده از سرور
            try:
                response = requests.get(f"{SERVER_URL}{current_ts}", timeout=5)
                response.raise_for_status()
                # The response text is the formatted log entry: <timestamp> <date>
                # متن پاسخ همان ورودی لاگ فرمت شده است: <timestamp> <date>
                log_entry = response.text.strip()
                
                # 3. Put the log entry into the queue (unsorted)
                # 3. قرار دادن ورودی لاگ در صف (نامرتب)
                log_queue.put(log_entry)
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching timestamp from server: {e}")

            time.sleep(1) # Log once per second
            
        logger.info("Finished logging.")

# --- Log Sorter and Writer ---
# --- مرتب ساز و نویسنده لاگ ---
def sort_and_write_logs():
    """
    Retrieves all logs from the queue, sorts them by timestamp, and writes them to a file.
    تمام لاگ‌ها را از صف بازیابی کرده، بر اساس timestamp مرتب کرده و در فایل می‌نویسد.
    """
    
    # Wait for all logs to be written to the queue
    # صبر کردن تا تمام لاگ‌ها در صف نوشته شوند
    log_queue.join()
    
    all_logs = []
    # Extract all items from the queue
    # استخراج تمام آیتم‌ها از صف
    while not log_queue.empty():
        all_logs.append(log_queue.get_nowait())

    # Sorting key: the timestamp is the first element of the log entry (separated by space)
    # کلید مرتب‌سازی: timestamp اولین عنصر ورودی لاگ است (جدا شده با فاصله)
    def get_timestamp(log_entry):
        try:
            return int(log_entry.split(' ')[0])
        except (ValueError, IndexError):
            return 0

    # Sort the logs
    # مرتب‌سازی لاگ‌ها
    sorted_logs = sorted(all_logs, key=get_timestamp)
    
    # Write sorted logs to file
    # نوشتن لاگ‌های مرتب شده در فایل
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        for entry in sorted_logs:
            f.write(entry + '\n')
            
    logger.info(f"Successfully wrote {len(sorted_logs)} sorted logs to {LOG_FILE}.")


# --- Main Function ---
# --- تابع اصلی ---
def main():
    threads = []
    
    # 1. Start threads sequentially with a 1-second interval
    # 1. شروع نخ‌ها به صورت متوالی با فاصله 1 ثانیه
    for i in range(NUM_THREADS):
        worker = LogWorker(name=f"Worker-{i+1}")
        threads.append(worker)
        worker.start()
        time.sleep(1) # Start next thread 1 second later

    # 2. Wait for all logging threads to finish
    # 2. صبر کردن تا تمام نخ‌های لاگ‌گیری به پایان برسند
    for t in threads:
        t.join()
        
    # 3. Sort and write the collected logs
    # 3. مرتب‌سازی و نوشتن لاگ‌های جمع‌آوری شده
    sort_and_write_logs()

if __name__ == '__main__':
    # NOTE: server.py must be running on http://127.0.0.1:8080 before running this script!
    # توجه: server.py باید قبل از اجرای این اسکریپت روی http://127.0.0.1:8080 در حال اجرا باشد!
    main()
