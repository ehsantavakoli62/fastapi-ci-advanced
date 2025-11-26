# cat_downloader_comparison.py

import requests
import os
import time
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List

# پوشه ذخیره فایل‌ها
DOWNLOAD_DIR = "cats"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# کدهای وضعیت HTTP برای دانلود
CAT_STATUS_CODES = [200, 201, 202, 301, 400, 401, 403, 404, 500, 503]


# --- A. پیاده‌سازی مسدودکننده (Blocking) برای Threads و Processes ---

def blocking_download_and_save(cat_id: int):
    """
    دانلود و ذخیره مسدودکننده (Blocking) که برای Threads و Processes استفاده می‌شود.
    """
    url = f"https://http.cat/{cat_id}"
    filename = os.path.join(DOWNLOAD_DIR, f"cat_{cat_id}.jpg")
    
    # print(f"Downloading {url}...")

    try:
        # درخواست مسدودکننده با requests
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # عملیات I/O مسدودکننده
        with open(filename, 'wb') as f:
            f.write(response.content)
            
        return f"Cat {cat_id} saved."
    
    except Exception as e:
        return f"Failed to download {url}: {e}"

# --- B. پیاده‌سازی آسنکرون (Coroutine) ---

async def async_download_and_save(session: aiohttp.ClientSession, cat_id: int):
    """
    پیاده‌سازی آسنکرون (از تمرین ۱) برای مقایسه.
    """
    url = f"https://http.cat/{cat_id}"
    filename = os.path.join(DOWNLOAD_DIR, f"cat_{cat_id}_async.jpg")
    
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                
                # استفاده از asyncio.to_thread برای I/O آسنکرون در فایل
                await asyncio.to_thread(lambda: open(filename, 'wb').write(content))
                return f"Cat {cat_id} saved (async)."
            else:
                return f"Failed to download {url} (async). Status: {response.status}"
    except Exception as e:
        return f"An error occurred while processing {url} (async): {e}"


# --- C. توابع اصلی برای اجرای مقایسه‌ای ---

def run_threads(ids: List[int]):
    """اجرا با ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=32) as executor:
        results = list(executor.map(blocking_download_and_save, ids))
    # print("\n".join(results))

def run_processes(ids: List[int]):
    """اجرا با ProcessPoolExecutor."""
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
        results = list(executor.map(blocking_download_and_save, ids))
    # print("\n".join(results))

async def run_async(ids: List[int]):
    """اجرا با asyncio و aiohttp."""
    async with aiohttp.ClientSession() as session:
        tasks = [async_download_and_save(session, cat_id) for cat_id in ids]
        await asyncio.gather(*tasks)

# --- D. تابع اجرای مقایسه‌ای و ساخت جدول ---

def compare_performance(image_counts: List[int]):
    """اجرای تست‌ها و نمایش نتایج در جدول Markdown."""
    results = []
    
    for count in image_counts:
        # ساخت لیست IDها
        ids_to_download = (CAT_STATUS_CODES * ((count // len(CAT_STATUS_CODES)) + 1))[:count]
        
        row = {'Count': count}

        # 1. تست Async
        start = time.time()
        asyncio.run(run_async(ids_to_download))
        end = time.time()
        row['Async (to_thread)'] = f"{end - start:.2f} s"
        
        # 2. تست Threads
        start = time.time()
        run_threads(ids_to_download)
        end = time.time()
        row['Threads'] = f"{end - start:.2f} s"

        # 3. تست Processes
        start = time.time()
        run_processes(ids_to_download)
        end = time.time()
        row['Processes'] = f"{end - start:.2f} s"
        
        results.append(row)

    # ساخت جدول Markdown
    table_output = "## 📊 جدول مقایسه عملکرد دانلود تصویر\n\n"
    table_output += "| تعداد تصاویر | آسنکرون (Coroutines + to\_thread) | Threading (I/O Bound) | Multiprocessing (CPU Bound) |\n"
    table_output += "| :------------: | :-------------------------------: | :----------------------: | :---------------------------: |\n"
    
    for row in results:
        table_output += f"| {row['Count']} | {row['Async (to_thread)']} | {row['Threads']} | {row['Processes']} |\n"
        
    print(table_output)
    print("\n--- نکته تحلیلی ---\nدر عملیات I/O-Bound (مانند دانلود از شبکه)، انتظار می‌رود روش‌های Async و Threading بهترین عملکرد را داشته باشند، زیرا گلوگاه اصلی زمان انتظار است و نیازی به سربار تعویض فرآیند (Process Switching) نیست.")


if __name__ == "__main__":
    # اجرا با تعداد تصاویر درخواستی
    image_counts = [10, 50, 100]
    compare_performance(image_counts)
