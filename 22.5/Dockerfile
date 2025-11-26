# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# دستور پیش‌فرض را خالی می‌گذاریم و در docker-compose تعریف می‌کنیم
CMD ["/bin/bash"]
