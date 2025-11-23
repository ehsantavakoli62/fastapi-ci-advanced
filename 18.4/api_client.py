# api_client.py

import requests
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
# برای دیدن جزئیات اتصال HTTP، سطح DEBUG را فعال کنید
logging.getLogger().setLevel(logging.DEBUG) 

class APIClient:
    """A client for testing API performance with Session and ThreadPool."""
    
    BASE_URL = "http://127.0.0.1:5000/api/authors/" 
    
    # Payload برای POST
    AUTHOR_PAYLOAD: Dict[str, Any] = {
        "first_name": "تستر",
        "last_name": str(time.time()), # برای اطمینان از منحصر به فرد بودن
    }

    def __init__(self, use_session: bool = False):
        self.use_session = use_session
        self._session = requests.Session() if use_session else None
        # استفاده از requests.Session یا requests
        self.client = self._session if use_session else requests
        
    def _send_request(self):
        """Sends a single POST request to the API."""
        # تغییر last_name برای جلوگیری از خطای تکراری در عمل
        payload = {"first_name": "تستر", "last_name": str(time.time())} 
        try:
            response = self.client.post(self.BASE_URL, json=payload, timeout=5)
            # فقط لاگ سطح DEBUG
            logging.debug(f"Request status: {response.status_code}") 
            return response.elapsed.total_seconds()
        except requests.exceptions.RequestException as e:
            logging.debug(f"Request failed: {e}")
            return None

    def run_sequential_test(self, num_requests: int) -> float:
        """Executes requests sequentially."""
        start_time = time.time()
        for _ in range(num_requests):
            self._send_request()
        return time.time() - start_time

    def run_concurrent_test(self, num_requests: int) -> float:
        """Executes requests concurrently using ThreadPoolExecutor."""
        start_time = time.time()
        
        # استفاده از Threads (ThreadPoolExecutor) برای موازی‌سازی
        with ThreadPoolExecutor(max_workers=20) as executor: 
            # ارسال وظایف
            futures = [executor.submit(self._send_request) for _ in range(num_requests)]
            
            # منتظر ماندن برای تکمیل تمام رشته‌ها
            for future in as_completed(futures):
                future.result() 
                
        return time.time() - start_time


def conduct_experiment(num_requests: int, use_session: bool, use_threads: bool, test_name: str) -> float:
    """Runs a single test case and returns execution time."""
    client = APIClient(use_session=use_session)
    if use_threads:
        time_taken = client.run_concurrent_test(num_requests)
    else:
        time_taken = client.run_sequential_test(num_requests)
        
    logging.info(f"Test {test_name} ({num_requests} reqs): {time_taken:.4f}s")
    return time_taken


if __name__ == '__main__':
    # !!! توجه: قبل از اجرای این بخش، مطمئن شوید که app.py در حال اجرا است !!!
    
    REQUEST_COUNTS = [10, 100, 1000]
    results = {}
    
    # این نتایج فقط برای ستون‌های "+O" (با تنظیم WSGIRequestHandler) معتبر است.
    # برای ستون‌های "-O" باید app.py را بدون آن تنظیم مجدداً اجرا کنید.
    print("--- Running Experiments (+O Column) ---")
    
    for count in REQUEST_COUNTS:
        results[count] = {}
        
        # -S -T : بدون Session، بدون Threads
        results[count]['S-T-'] = conduct_experiment(count, False, False, '-S -T')
        
        # +S -T : با Session، بدون Threads
        results[count]['S+T-'] = conduct_experiment(count, True, False, '+S -T')
        
        # -S +T : بدون Session، با Threads
        results[count]['S-T+'] = conduct_experiment(count, False, True, '-S +T')
        
        # +S +T : با Session، با Threads
        results[count]['S+T+'] = conduct_experiment(count, True, True, '+S +T')
        
    # نمایش نتایج برای پر کردن جدول REPORT.md
    print("\n--- Results Table for +O Columns ---")
    print(f"{'Count':<8} | {'-S -T':<8} | {'+S -T':<8} | {'-S +T':<8} | {'+S +T':<8}")
    print("-" * 45)
    for count, res in results.items():
        print(f"{count:<8} | {res['S-T-']:.4f} | {res['S+T-']:.4f} | {res['S-T+']:.4f} | {res['S+T+']:.4f}")
