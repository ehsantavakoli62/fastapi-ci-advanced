# wsgi_server.py

# این فایل فقط برای اشاره به برنامه WSGI در routes.py استفاده می‌شود
from routes import app as application

# در محیط واقعی، شما این فایل را با Gunicorn اجرا می‌کنید:
# gunicorn wsgi_server:application -b 127.0.0.1:8000
