import logging
import random
import threading
import time

# Global variables
# متغیرهای سراسری
TOTAL_TICKETS = 10 
MAX_CAPACITY = 100 # Maximum number of seats/tickets allowed in total
SELLER_COUNT = 4 # Number of sellers/cashiers
TICKET_THRESHOLD = SELLER_COUNT + 1 # Threshold to trigger printing (e.g., when tickets <= 4, Director prints)
PRINT_AMOUNT = 6 # Amount of tickets the Director prints each time

# Basic logging configuration
# تنظیمات پایه لاگ
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s: %(message)s')
logger = logging.getLogger(__name__)

# --- Seller Class (Updated) ---
# --- کلاس فروشنده (به‌روز شده) ---
class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore):
        super().__init__()
        self.sem = semaphore
        self.tickets_sold = 0
        logger.info(f'Seller started work with {TOTAL_TICKETS} tickets available.')

    def run(self):
        global TOTAL_TICKETS
        while True:
            self.random_sleep()
            
            # Use semaphore to access the shared resource (TOTAL_TICKETS)
            # استفاده از سمافور برای دسترسی به منبع مشترک (TOTAL_TICKETS)
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.getName()} sold one ticket. {TOTAL_TICKETS} left.')

        logger.info(f'Seller {self.getName()} sold {self.tickets_sold} tickets and finished.')

    def random_sleep(self):
        # Shorter sleep to make the Director's printing noticeable
        # استراحت کوتاه‌تر تا چاپ کردن مدیر قابل توجه باشد
        time.sleep(random.uniform(0.1, 0.5)) 

# --- Director/Printer Class (NEW) ---
# --- کلاس مدیر/چاپخانه (جدید) ---
class Director(threading.Thread):
    
    def __init__(self, semaphore: threading.Semaphore):
        super().__init__(name="Director-Printer")
        self.sem = semaphore
        self.total_printed = 0
        logger.info('Director started monitoring the tickets.')

    def run(self):
        global TOTAL_TICKETS
        global MAX_CAPACITY
        
        while TOTAL_TICKETS < MAX_CAPACITY:
            self.random_sleep()
            
            # Check if tickets are below the threshold
            # بررسی اینکه آیا بلیط‌ها زیر آستانه هستند
            if TOTAL_TICKETS <= TICKET_THRESHOLD:
                
                # Use semaphore to access the shared resource (TOTAL_TICKETS)
                # استفاده از سمافور برای دسترسی انحصاری به TOTAL_TICKETS (هم فروشندگان و هم مدیر)
                with self.sem:
                    # Double-check condition inside the locked block
                    # بررسی مجدد شرط در داخل بلوک قفل شده
                    if TOTAL_TICKETS <= TICKET_THRESHOLD and TOTAL_TICKETS < MAX_CAPACITY:
                        
                        tickets_to_print = PRINT_AMOUNT
                        # Ensure not to exceed max capacity
                        # اطمینان حاصل شود که از حداکثر ظرفیت تجاوز نکند
                        if TOTAL_TICKETS + tickets_to_print > MAX_CAPACITY:
                            tickets_to_print = MAX_CAPACITY - TOTAL_TICKETS
                        
                        TOTAL_TICKETS += tickets_to_print
                        self.total_printed += tickets_to_print
                        logger.warning(f'--- DIRECTOR PRINTS: Added {tickets_to_print} tickets. Total is now {TOTAL_TICKETS}. ---')
                        
                    elif TOTAL_TICKETS >= MAX_CAPACITY:
                         logger.info('MAX CAPACITY REACHED. Stopping printing.')
                         break # Stop director if max capacity is reached

        logger.info(f'Director {self.getName()} finished, total printed: {self.total_printed}')

    def random_sleep(self):
        # Director is slower than sellers
        # مدیر کندتر از فروشندگان است
        time.sleep(random.uniform(1, 3)) 

# --- Main Function ---
# --- تابع اصلی ---
def main():
    # Semaphore with capacity 3 (three open cashiers)
    # سمافور با ظرفیت 3 (سه صندوق باز)
    semaphore = threading.Semaphore(3) 
    
    # 1. Start Sellers
    # 1. شروع فروشندگان
    sellers = []
    for i in range(SELLER_COUNT):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)

    # 2. Start Director
    # 2. شروع مدیر
    director = Director(semaphore)
    director.start()

    # 3. Wait for all to finish
    # 3. انتظار برای اتمام کار همه
    for seller in sellers:
        seller.join()
        
    director.join()

    logger.info(f'\n--- Final Report ---')
    logger.info(f'All sellers finished. Total tickets remaining: {TOTAL_TICKETS}')

if __name__ == '__main__':
    main()
