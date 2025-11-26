# tasks.py

from celery import Celery, chain, group
from celery.utils.log import get_task_logger
from datetime import timedelta
from typing import List
import time
import requests
from io import BytesIO
from PIL import Image, ImageFilter
from database import get_all_subscribers, get_all_subscribers_emails

logger = get_task_logger(__name__)

# --- 1. تعریف اپلیکیشن Celery و تنظیمات ---
# فرض بر این است که Redis در آدرس localhost:6379 در دسترس است
celery_app = Celery(
    'image_processor',
    broker='redis://redis:6379/0', # استفاده از نام سرویس 'redis' در محیط Docker
    backend='redis://redis:6379/0'
)

celery_app.conf.update(
    # تنظیمات برای Celery Beat (خبرنامه هفتگی)
    CELERYBEAT_SCHEDULE = {
        'send-weekly-newsletter': {
            'task': 'tasks.send_weekly_newsletter',
            'schedule': timedelta(days=7), # هر ۷ روز یکبار
            'args': ()
        },
    },
    CELERY_TIMEZONE = 'UTC',
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_ENABLE_UTC = True,
)

# --- 2. توابع شبیه‌سازی (Simulation Functions) ---

def process_image_and_return_url(image_url: str) -> str:
    """
    شبیه‌سازی دانلود، اعمال اثر Blur و آپلود مجدد.
    """
    logger.info(f"Processing image: {image_url}")
    
    # 1. دانلود تصویر
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
    except Exception as e:
        logger.error(f"Failed to download/open image {image_url}: {e}")
        raise

    # 2. اعمال افکت (Blur)
    blurred_img = img.filter(ImageFilter.BLUR)
    
    # 3. شبیه‌سازی آپلود و ساخت URL جدید
    # در اینجا فقط زمان می‌گیرد تا شبیه‌سازی پردازش سنگین باشد.
    time.sleep(5) 
    
    # آدرس URL شبیه‌سازی شده
    new_url = f"processed_{uuid.uuid4()}.jpg" 
    logger.info(f"Finished processing image {image_url}. New URL: {new_url}")
    return new_url

def send_email(recipient: str, subject: str, body: str):
    """
    شبیه‌سازی ارسال ایمیل.
    """
    logger.info(f"Sending email to {recipient} with subject: {subject}")
    # شبیه‌سازی تأخیر در ارسال
    time.sleep(2)
    logger.info(f"Email sent successfully to {recipient}.")


# --- 3. وظایف Celery ---

@celery_app.task
def process_single_image(image_url: str, user_email: str) -> str:
    """
    وظیفه پردازش یک تصویر.
    """
    new_url = process_image_and_return_url(image_url)
    
    # ارسال ایمیل به محض آماده شدن تصویر
    subject = "Image Processing Complete"
    body = f"Your image is ready! You can find it at: {new_url}"
    send_email(user_email, subject, body)
    
    return new_url

@celery_app.task
def send_completion_notification(processed_results: List[str], user_email: str):
    """
    وظیفه نهایی: ارسال ایمیل جمع‌بندی (اگرچه در تمرین گفته شده "به محض آماده شدن").
    این وظیفه نشان‌دهنده استفاده از Celery Chain است.
    """
    logger.info(f"All images processed for {user_email}. Sending final summary.")
    
    # در اینجا می‌توانستیم تصاویر را زیپ کرده و بفرستیم.
    summary_body = "All your images have been processed:\n" + "\n".join(processed_results)
    send_email(user_email, "Final Image Processing Summary", summary_body)


@celery_app.task
def blur_images_group(image_urls: List[str], user_email: str):
    """
    وظیفه گروهی که وظایف پردازش تکی را ایجاد می‌کند.
    """
    # ایجاد یک گروه از وظایف process_single_image
    task_group = group([process_single_image.s(url, user_email) for url in image_urls])
    
    # استفاده از chain (زنجیره) برای اجرای یک وظیفه پس از اتمام گروه (Callback)
    # chain(task_group, send_completion_notification.s(user_email)).apply_async()
    
    # یا فقط اجرای گروه (برای ساده‌سازی پیگیری وضعیت)
    return task_group.apply_async()


@celery_app.task
def send_weekly_newsletter():
    """
    وظیفه زمان‌بندی شده Celery Beat: ارسال خبرنامه هفتگی.
    """
    logger.info("Starting weekly newsletter dispatch.")
    subscribers = get_all_subscribers_emails()
    
    if not subscribers:
        logger.info("No subscribers found. Newsletter skipped.")
        return

    subject = "Weekly Service Update: Check out our new features!"
    body = "Thank you for using our image processing service. We have processed X images this week."
    
    # ایجاد یک گروه از وظایف ارسال ایمیل
    email_tasks = group([send_email.s(email, subject, body) for email in subscribers])
    email_tasks.apply_async()
    
    logger.info(f"Dispatched newsletter to {len(subscribers)} subscribers.")
