import logging
import threading
import random
import time

# Basic logging configuration in English
# تنظیمات پایه لاگ به زبان انگلیسی
logging.basicConfig(level='INFO', format='%(threadName)s: %(message)s')
logger = logging.getLogger(__name__)

class Philosopher(threading.Thread):
    # Class-level flag to control all threads
    # پرچم سطح کلاس برای کنترل تمام نخ‌ها
    running = True

    def __init__(self, name: str, left_fork: threading.Lock, right_fork: threading.Lock):
        super().__init__(name=name)
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        while self.running:
            # Philosopher starts thinking
            # فیلسوف شروع به تفکر می‌کند
            logger.info('start thinking.')
            time.sleep(random.uniform(1, 4))
            logger.info('is hungry.')
            
            # --- USING CONTEXT MANAGER (The required solution) ---
            # --- استفاده از Context Manager (راه حل مورد نیاز تمرین) ---
            
            # Acquire the left fork
            # گرفتن چنگال سمت چپ
            with self.left_fork:
                logger.info('acquired left fork')
                
                # Check right fork state to prevent deadlock
                # بررسی وضعیت چنگال راست برای جلوگیری از Deadlock
                if self.right_fork.locked():
                    continue 

                # Acquire the right fork
                # گرفتن چنگال سمت راست
                with self.right_fork:
                    logger.info('acquired right fork')
                    self.dining()
            
            # Both forks are automatically released upon exiting the 'with' blocks.
            # هر دو چنگال به طور خودکار پس از خروج از بلوک‌های 'with' آزاد می‌شوند.

    def dining(self):
        # Eating process
        # فرآیند غذا خوردن
        logger.info('starts eating.')
        time.sleep(random.uniform(1, 4))
        logger.info('finishes eating and leaves to think.')

def main():
    NUM_PHILOSOPHERS = 5
    
    # Create 5 Locks (forks)
    # ایجاد 5 قفل (چنگال)
    forks = [threading.Lock() for n in range(NUM_PHILOSOPHERS)]
    
    # Create 5 philosophers
    # ایجاد 5 فیلسوف
    philosophers = [
        Philosopher(f'Philosopher-{i+1}', forks[i % NUM_PHILOSOPHERS], forks[(i + 1) % NUM_PHILOSOPHERS])
        for i in range(NUM_PHILOSOPHERS)
    ]
    
    Philosopher.running = True
    for p in philosophers:
        p.start()
        
    time.sleep(20) 
    
    Philosopher.running = False
    logger.info("Now we're finishing.")
    
    for p in philosophers:
        p.join()

if __name__ == "__main__":
    main()
