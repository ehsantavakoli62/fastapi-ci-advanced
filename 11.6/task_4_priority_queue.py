import threading
import queue
import time
import random
import logging

# Basic logging configuration
# تنظیمات پایه لاگ
logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')
logger = logging.getLogger(__name__)

# --- Task Model ---
# --- مدل وظیفه ---
class Task:
    """
    Represents a task with a priority, a function to execute, and its arguments.
    یک وظیفه را با اولویت، تابع اجرایی و آرگومان‌های آن نمایش می‌دهد.
    """
    def __init__(self, priority: int, func, args=None):
        self.priority = priority
        self.func = func
        self.args = args or ()

    # The comparison method is necessary for PriorityQueue to work.
    # متد مقایسه برای کارکرد PriorityQueue ضروری است.
    def __lt__(self, other):
        # Defines less-than based on priority (lower number means higher priority)
        # کمتر بودن را بر اساس اولویت تعریف می‌کند (عدد کوچکتر = اولویت بالاتر)
        return self.priority < other.priority

    def __repr__(self):
        # String representation for printing
        # نمایش رشته‌ای برای چاپ
        return f"Task(priority={self.priority}). \t\tsleep({self.args[0]})"

    def execute(self):
        # Executes the stored function with its arguments
        # تابع ذخیره شده را با آرگومان‌هایش اجرا می‌کند
        logger.info(f">running {self}")
        self.func(*self.args)

# --- Producer Thread ---
# --- نخ تولید کننده ---
class Producer(threading.Thread):
    
    def __init__(self, name: str, task_queue: queue.PriorityQueue, num_tasks: int):
        super().__init__(name=name)
        self.task_queue = task_queue
        self.num_tasks = num_tasks

    def run(self):
        logger.info('Running')
        
        # 1. Define possible functions (simple time.sleep for demonstration)
        # 1. تعریف توابع ممکن (time.sleep ساده برای نمایش)
        functions = [time.sleep] 
        
        # 2. Generate and put tasks into the queue
        # 2. تولید و قرار دادن وظایف در صف
        for i in range(self.num_tasks):
            # Priorities range from 0 (highest) to 6 (lowest)
            # اولویت‌ها از 0 (بالاترین) تا 6 (پایین‌ترین) متغیر هستند
            priority = random.randint(0, 6) 
            
            # Sleep time for the task
            # زمان استراحت برای وظیفه
            sleep_time = random.random() * 0.9 + 0.1 
            
            task = Task(priority, random.choice(functions), args=(sleep_time,))
            
            # The item put into PriorityQueue must be a tuple: (priority, item) 
            # or the item itself if it implements __lt__ (which our Task does).
            # آیتمی که در PriorityQueue قرار می‌گیرد باید یک تاپل باشد: (اولویت، آیتم) 
            # یا خود آیتم اگر متد __lt__ را پیاده‌سازی کرده باشد (که کلاس Task ما این کار را می‌کند).
            self.task_queue.put(task)
        
        logger.info('Done')

# --- Consumer Thread ---
# --- نخ مصرف کننده ---
class Consumer(threading.Thread):
    
    def __init__(self, name: str, task_queue: queue.PriorityQueue):
        super().__init__(name=name)
        self.task_queue = task_queue

    def run(self):
        logger.info('Running')
        
        # Keep running until the queue is empty AND all tasks reported done
        # تا زمانی که صف خالی شود و همه وظایف انجام شده گزارش شوند، ادامه دهید
        while True:
            try:
                # Get task with the highest priority (blocking call)
                # گرفتن وظیفه با بالاترین اولویت (فراخوانی بلوک کننده)
                task = self.task_queue.get(timeout=1) # Timeout added to prevent infinite block
                
                task.execute()
                
                # Signal that the task is complete
                # سیگنال دادن که وظیفه کامل شده است
                self.task_queue.task_done()
                
            except queue.Empty:
                # Exit loop if queue is empty after timeout
                # خروج از حلقه اگر صف پس از زمان انتظار خالی باشد
                break

        logger.info('Done')

# --- Main Execution ---
# --- اجرای اصلی ---
def main():
    TASK_COUNT = 10 # Number of tasks to generate
    
    # Initialize the Priority Queue
    # مقداردهی اولیه صف اولویت
    task_queue = queue.PriorityQueue()
    
    # Initialize threads
    # مقداردهی اولیه نخ‌ها
    producer = Producer("Producer", task_queue, TASK_COUNT)
    consumer = Consumer("Consumer", task_queue)
    
    # Start threads
    # شروع نخ‌ها
    producer.start()
    consumer.start()
    
    # Wait for the Producer to finish adding all tasks
    # صبر کردن تا Producer تمام وظایف را اضافه کند
    producer.join() 
    
    # Wait for the Consumer to finish processing all tasks
    # صبر کردن تا Consumer تمام وظایف را پردازش کند
    # queue.join() blocks until all items in the queue have been retrieved and processed
    # queue.join() تا زمانی که تمام آیتم‌ها از صف بازیابی و پردازش شوند، مسدود می‌شود
    task_queue.join() 
    
    # Wait for the Consumer thread to gracefully exit its run loop
    # صبر کردن تا نخ Consumer به آرامی از حلقه اجرای خود خارج شود
    consumer.join() 

if __name__ == '__main__':
    main()
