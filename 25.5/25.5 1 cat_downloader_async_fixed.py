# cat_downloader_async_fixed.py

import asyncio
import aiohttp
import os
import time

# پوشه ذخیره فایل‌ها
DOWNLOAD_DIR = "cats"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

async def download_cat_image(session: aiohttp.ClientSession, cat_id: int):
    """
    دانلود یک تصویر گربه به صورت آسنکرون و ذخیره آن.
    """
    url = f"https://http.cat/{cat_id}"
    filename = os.path.join(DOWNLOAD_DIR, f"cat_{cat_id}.jpg")
    
    print(f"Downloading {url}...")

    try:
        # درخواست آسنکرون با aiohttp
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                
                # --- جایگزینی aiofiles با open و asyncio.to_thread ---
                # تابع open یک عملیات مسدودکننده (Blocking) است.
                # برای اجرای آن به صورت آسنکرون، آن را به یک ترد مجزا می‌فرستیم
                # تا Event Loop مسدود نشود.
                def blocking_write():
                    with open(filename, 'wb') as f:
                        f.write(content)

                # اجرای تابع مسدودکننده در یک ترد (Thread Pool)
                await asyncio.to_thread(blocking_write)
                # --------------------------------------------------------
                
                print(f"Successfully saved {filename}")
                return True
            else:
                print(f"Failed to download {url}. Status: {response.status}")
                return False

    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return False

async def main_task(image_count: int):
    """
    برنامه اصلی برای اجرای همزمان دانلودها.
    """
    # لیست کدهای وضعیت HTTP که با تصویر گربه نشان داده می‌شوند
    cat_status_codes = [200, 201, 202, 301, 400, 401, 403, 404, 500, 503]
    
    # برای تنوع، از لیست کدها به تعداد image_count کپی می‌کنیم
    ids_to_download = (cat_status_codes * ((image_count // len(cat_status_codes)) + 1))[:image_count]

    start_time = time.time()
    
    # استفاده از aiohttp.ClientSession برای مدیریت اتصالات
    async with aiohttp.ClientSession() as session:
        # ایجاد لیست وظایف (Tasks)
        tasks = [download_cat_image(session, cat_id) for cat_id in ids_to_download]
        
        # اجرای همزمان تمام وظایف
        await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"\n--- Async (to_thread) implementation completed in {end_time - start_time:.2f} seconds ---")

if __name__ == "__main__":
    # اجرای 10 تصویر برای تست
    asyncio.run(main_task(10))
