# api_client.py

import requests
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Literal

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class APIClient:
    """A client for testing API performance."""
    
    BASE_URL = "http://127.0.0.1:5000/api/authors/" 
    
    # Payload برای POST
    AUTHOR_PAYLOAD = {
        "first_name": "تستر",
        "last_name": "سرعت",
        "middle_name": "و زمان"
    }

    def __init__(self, use_session: bool = False):
        self.use_session = use_session
        self._session = requests.Session() if use_session else None
        self.client = self._session if use_session else requests
        
    def _send_request(self):
        """Sends a single POST request to the API."""
        try:
            # استفاده از POST ساده به عنوان نمونه (می‌توان GET را نیز تست کرد)
            response = self.client.post(self.BASE_URL, json=self.AUTHOR_PAYLOAD)
            # اگر از session استفاده نشود، client همان requests است
            if response.status_code not in (201, 409): # 409 در صورت تکراری بودن نویسنده (که در این تست مهم نیست)
                 logging.debug(f"Request failed with status: {response.status_code}")
            return response.status_code
        except requests.exceptions.RequestException as e:
            logging.debug(f"Request failed: {e}")
            return None

    def run_sequential_test(self, num_requests: int) -> float:
        """Executes requests sequentially."""
        start_time = time.time()
        for _ in range(num_requests):
            self._send_request()
        end_time = time.time()
        return end_time - start_time

    def run_concurrent_test(self, num_requests: int) -> float:
        """Executes requests concurrently using ThreadPoolExecutor."""
        start_time = time.time()
        
        # استفاده از ۱۰ رشته برای موازی‌سازی
        with ThreadPoolExecutor(max_workers=10) as executor: 
            futures = [executor.submit(self._send_request) for _ in range(num_requests)]
            
            # منتظر ماندن برای تکمیل تمام رشته‌ها
            for future in as_completed(futures):
                future.result() 
                
        end_time = time.time()
        return end_time - start_time


def conduct_experiment(num_requests: int, use_session: bool, use_threads: bool, test_name: str) -> float:
    """Runs a single test case and returns execution time."""
    client = APIClient(use_session=use_session)
    if use_threads:
        time_taken = client.run_concurrent_test(num_requests)
    else:
        time_taken = client.run_sequential_test(num_requests)
        
    logging.info(f"Test {test_name} ({num_requests} requests, Session: {use_session}, Threads: {use_threads}): {time_taken:.4f}s")
    return time_taken


if __name__ == '__main__':
    # توجه: قبل از اجرای این بخش، مطمئن شوید که app.py در حال اجرا است
    
    # تنظیم DEBUG برای دیدن جزئیات اتصال
    logging.getLogger().setLevel(logging.DEBUG) 

    REQUEST_COUNTS = [10, 100, 1000]
    
    results = {}
    
    # شبیه‌سازی دو حالت: با (+O) و بدون (-O) تنظیم WSGIRequestHandler
    # توجه: شما باید این تست‌ها را دو بار اجرا کنید: یک بار با تنظیم و یک بار بدون تنظیم WSGIRequestHandler در app.py
    
    print("--- Running Experiments (Assuming WSGIRequestHandler.protocol_version = 'HTTP/1.1' is active for +O columns) ---")
    
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
    print("\n--- Results for REPORT.md (+O Column) ---")
    print(f"{'Count':<8} | {'-S -T':<8} | {'+S -T':<8} | {'-S +T':<8} | {'+S +T':<8}")
    print("-" * 45)
    for count, res in results.items():
        print(f"{count:<8} | {res['S-T-']:.4f} | {res['S+T-']:.4f} | {res['S-T+']:.4f} | {res['S+T+']:.4f}")
