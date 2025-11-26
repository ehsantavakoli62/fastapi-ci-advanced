# app.py

import uuid
from flask import Flask, request, jsonify
from celery.result import AsyncResult, GroupResult
from tasks import blur_images_group, send_weekly_newsletter, celery_app
from database import subscribe_user, unsubscribe_user, get_all_subscribers
from typing import List

app = Flask(__name__)

# --- 1. رووت‌های اصلی ---

# POST /blur
@app.route('/blur', methods=['POST'])
def blur_endpoint():
    """
    دریافت لیست تصاویر (آدرس‌های URL) و آدرس ایمیل کاربر.
    وظیفه پردازش آسنکرون تصاویر را در Celery ایجاد می‌کند.
    """
    data = request.get_json()
    image_urls: List[str] = data.get('image_urls', [])
    user_email: str = data.get('email', '')

    if not image_urls or not user_email:
        return jsonify({"error": "Missing image_urls or email"}), 400

    # ارسال وظیفه گروهی به Celery (group of tasks)
    task_group: GroupResult = blur_images_group.delay(image_urls, user_email)
    
    # شناسه گروه وظایف (Group ID) برای پیگیری وضعیت
    return jsonify({"group_id": task_group.id, "message": "Image processing started"}), 202

# GET /status/<id>
@app.route('/status/<id>', methods=['GET'])
def status_endpoint(id: str):
    """
    بررسی وضعیت یک وظیفه گروهی (group_id) Celery.
    """
    task_group: GroupResult = AsyncResult(id, app=celery_app)
    
    if task_group.status == 'PENDING':
        return jsonify({"status": "PENDING", "progress": 0, "total": 0}), 200

    # اگر وظیفه گروهی تکمیل شده است
    if task_group.ready():
        status = "COMPLETED"
    else:
        status = "IN_PROGRESS"
    
    # محاسبه تعداد وظایف تکمیل شده
    processed_count = task_group.completed_count() if task_group.successful() or task_group.failed() else task_group.satisfied_count()
    total_count = len(task_group.children) if task_group.children else 0
    
    return jsonify({
        "status": status,
        "progress": processed_count,
        "total": total_count
    }), 200

# POST /subscribe
@app.route('/subscribe', methods=['POST'])
def subscribe_endpoint():
    """ثبت ایمیل کاربر برای خبرنامه هفتگی."""
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Missing email"}), 400
    
    try:
        subscribe_user(email)
        return jsonify({"message": f"Successfully subscribed: {email}"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409 # Conflict

# POST /unsubscribe
@app.route('/unsubscribe', methods=['POST'])
def unsubscribe_endpoint():
    """حذف ایمیل کاربر از خبرنامه."""
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Missing email"}), 400
    
    if unsubscribe_user(email):
        return jsonify({"message": f"Successfully unsubscribed: {email}"}), 200
    else:
        return jsonify({"error": f"Email not found: {email}"}), 404

# --- 2. رووت تستی برای اجرای دستی خبرنامه (اختیاری) ---
@app.route('/send_newsletter_now', methods=['POST'])
def send_newsletter_now_endpoint():
    """رووت کمکی برای اجرای دستی وظیفه Celery Beat."""
    task = send_weekly_newsletter.delay()
    return jsonify({"message": "Weekly newsletter task manually triggered", "task_id": task.id}), 202

if __name__ == '__main__':
    # این فقط برای تست محلی است. در داکر، از gunicorn استفاده می‌شود.
    app.run(debug=True, host='0.0.0.0', port=5000)
