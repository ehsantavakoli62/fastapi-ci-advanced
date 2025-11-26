# app.py

import time
from flask import Flask, jsonify, make_response
from prometheus_flask_exporter import PrometheusMetrics
import random

app = Flask(__name__)
# اتصال PrometheusMetrics به برنامه Flask
metrics = PrometheusMetrics(app)


# اندپوینت پیش‌فرض برای نمایش خودکار متریک‌های Flask
@app.route('/metrics', methods=['GET'])
@metrics.do_not_track() # متریک‌های Prometheus را از شمارش خودکار مستثنی می‌کند
def metrics_page():
    # این توسط خود PrometheusMetrics اداره می‌شود
    return make_response(metrics.export())


# --- متریک درخواستی: @metrics.counter() ---

# تعریف یک متریک سفارشی از نوع Counter
# این متریک به طور خودکار برچسب‌های متد (GET) و مسیر (/random_status) را اضافه می‌کند.
# برچسب status برای کد پاسخ (200، 404، و غیره) به طور خودکار توسط PrometheusMetrics اضافه می‌شود.
request_counter = metrics.counter(
    'requests_total_custom', 'Total number of requests to custom endpoints',
    labels={'endpoint': lambda: request.path}
)

@app.route('/random_status', methods=['GET'])
@request_counter # اعمال شمارنده سفارشی
def random_status_endpoint():
    """
    اندپوینتی که به صورت تصادفی کدهای پاسخ 200 یا 404 برمی‌گرداند.
    """
    time.sleep(0.1) # شبیه‌سازی کارکرد
    
    # 70% شانس برای کد 200، 30% شانس برای کد 404
    if random.random() < 0.7:
        return jsonify(message="Success"), 200
    else:
        return jsonify(message="Not Found"), 404
    
    
# --- اندپوینت‌های دیگر Flask برای تست ---

@app.route('/')
def home():
    return "Prometheus Monitoring Demo is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
