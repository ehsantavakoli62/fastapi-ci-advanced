# database.py

# شبیه‌سازی پایگاه داده: یک مجموعه (set) برای ذخیره ایمیل‌های یکتا
SUBSCRIPTIONS = set()

def subscribe_user(email: str):
    """کاربر را به لیست خبرنامه اضافه می‌کند."""
    if email in SUBSCRIPTIONS:
        raise ValueError(f"Email {email} is already subscribed.")
    SUBSCRIPTIONS.add(email)
    print(f"DEBUG: Subscribed: {email}") # برای لاگینگ کنسول

def unsubscribe_user(email: str) -> bool:
    """کاربر را از لیست خبرنامه حذف می‌کند."""
    if email in SUBSCRIPTIONS:
        SUBSCRIPTIONS.remove(email)
        print(f"DEBUG: Unsubscribed: {email}")
        return True
    return False

def get_all_subscribers() -> set:
    """لیست تمام مشترکین را برمی‌گرداند."""
    return SUBSCRIPTIONS

def get_all_subscribers_emails() -> List[str]:
    """لیست ایمیل‌ها را به فرمت لیست string برمی‌گرداند."""
    return list(SUBSCRIPTIONS)
