# async_crawler.py

import asyncio
import aiohttp
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from typing import Set, List, Tuple
import os
import re

# --- تنظیمات ---
MAX_DEPTH = 3 
OUTPUT_FILE = "found_external_links.txt"
VISITED_URLS: Set[str] = set()
EXTERNAL_LINKS: Set[str] = set()
MAIN_DOMAIN: str = ""


# --- توابع کمکی ---

def is_external(base_url: str, link_url: str) -> bool:
    """بررسی می‌کند آیا لینک مقصد یک لینک خارجی است."""
    # اطمینان از تعریف MAIN_DOMAIN
    if not MAIN_DOMAIN:
        return False
        
    parsed_link = urlparse(link_url)
    
    # لینک‌های بدون طرح (schema) یا هاست
    if not parsed_link.netloc:
        return False
        
    # بررسی کنید که آیا دامنه لینک مقصد با دامنه اصلی متفاوت است
    return parsed_link.netloc != MAIN_DOMAIN


def parse_and_find_links(base_url: str, html_content: str) -> Tuple[List[str], List[str]]:
    """
    HTML را پارس کرده و لینک‌های داخلی و خارجی را تفکیک می‌کند.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    internal_links = []
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        
        # حل آدرس‌های نسبی (مانند /about)
        full_url = urljoin(base_url, href)
        
        # حذف هش‌ها و پارامترهای تکراری برای جلوگیری از بازدید مجدد
        full_url = full_url.split('#')[0].split('?')[0] 
        
        # اگر طرح (schema) معتبر نیست، یا فقط anchor است، رد کنید
        if not full_url.startswith(('http://', 'https://')):
            continue
            
        if is_external(base_url, full_url):
            EXTERNAL_LINKS.add(full_url)
        else:
            internal_links.append(full_url)
            
    return internal_links


async def fetch_url(session: aiohttp.ClientSession, url: str) -> str:
    """
    محتوای URL را به صورت آسنکرون دریافت می‌کند.
    """
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                # محتوای متنی را برگردان
                return await response.text()
            else:
                print(f"Skipping {url}. Status: {response.status}")
                return ""
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""


async def recursive_crawler(session: aiohttp.ClientSession, url: str, depth: int):
    """
    تابع اصلی بازگشتی کراولر آسنکرون.
    """
    if depth > MAX_DEPTH:
        return

    if url in VISITED_URLS:
        return
    
    # برای جلوگیری از race condition، باید قبل از fetch، URL را اضافه کنیم
    VISITED_URLS.add(url)
    print(f"[{depth}/{MAX_DEPTH}] Visiting: {url}")
    
    html_content = await fetch_url(session, url)

    if html_content:
        # پارس HTML و یافتن لینک‌ها
        internal_links = parse_and_find_links(url, html_content)
        
        # ایجاد وظایف جدید برای لینک‌های داخلی (با عمق + 1)
        new_tasks = []
        for link in internal_links:
            if link not in VISITED_URLS:
                new_tasks.append(recursive_crawler(session, link, depth + 1))
        
        # اجرای همزمان تمام وظایف بازگشتی جدید
        if new_tasks:
            await asyncio.gather(*new_tasks)


async def main_crawler(start_urls: List[str]):
    """
    تنظیمات اولیه و راه‌اندازی فرآیند کراولینگ.
    """
    global MAIN_DOMAIN, VISITED_URLS, EXTERNAL_LINKS
    
    # تنظیم دامنه اصلی بر اساس اولین URL
    if start_urls:
        MAIN_DOMAIN = urlparse(start_urls[0]).netloc
    
    VISITED_URLS.clear()
    EXTERNAL_LINKS.clear()
    
    print(f"Crawler started with MAX_DEPTH={MAX_DEPTH}. Main domain: {MAIN_DOMAIN}")

    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        # ایجاد وظایف اولیه برای تمام URLهای شروع
        tasks = [recursive_crawler(session, url, depth=1) for url in start_urls]
        await asyncio.gather(*tasks)

    end_time = time.time()
    
    print(f"\n--- Crawling finished in {end_time - start_time:.2f} seconds ---")
    print(f"Found {len(EXTERNAL_LINKS)} external links.")

    # ذخیره لینک‌های خارجی در فایل
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for link in sorted(EXTERNAL_LINKS):
                f.write(link + '\n')
        print(f"External links saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error saving file: {e}")


if __name__ == "__main__":
    # مثال استفاده (می‌توانید MAX_DEPTH را تغییر دهید)
    start_urls_list = ["https://www.google.com/"] # یک دامنه فعال برای تست
    
    try:
        asyncio.run(main_crawler(start_urls_list))
    except KeyboardInterrupt:
        print("\nCrawler interrupted by user.")
