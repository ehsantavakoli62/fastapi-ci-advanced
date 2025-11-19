# log_server.py


from flask import Flask, request, jsonify, render_template_string
import logging
import json

# --- SERVER LOGGING SETUP ---
# برای جلوگیری از شلوغی، لاگ‌های خود Flask را محدود می‌کنیم.
# To prevent excessive output, we limit Flask's own logs.
server_logger = logging.getLogger('werkzeug')
server_logger.setLevel(logging.WARNING)

# --- GLOBAL LOG STORAGE ---
# ذخیره سازی جهانی لاگ‌ها (در واقعیت باید از دیتابیس استفاده شود)
# Global storage for collected logs (in reality, a database would be used)
collected_logs = []

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log_collector():
    """
    Receives log records via POST request (from HTTPHandler).
    لاگ‌ها را از طریق درخواست POST (از HTTPHandler) دریافت می‌کند.
    """
    if request.method == 'POST':
        # HTTPHandler sends data as form-data
        # HTTPHandler داده‌ها را به صورت form-data ارسال می‌کند
        log_data = dict(request.form)
        
        # Log the reception of the log message to the server console
        # لاگ دریافت پیام لاگ را در کنسول سرور ثبت می‌کند
        print(f"[SERVER RECEIVED]: {log_data.get('levelname', 'N/A')} - {log_data.get('name', 'N/A')} - {log_data.get('message', 'N/A')}")
        
        # Store the log data
        # ذخیره داده‌های لاگ
        collected_logs.append(log_data)
        return 'OK', 200
    
@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Returns all collected logs in JSON format.
    تمام لاگ‌های جمع‌آوری شده را در قالب JSON برمی‌گرداند.
    """
    return jsonify(collected_logs)


def run_server():
    """
    Starts the Flask server.
    سرور Flask را راه‌اندازی می‌کند.
    """
    # Host and port must match the HTTPHandler configuration
    # هاست و پورت باید با پیکربندی HTTPHandler مطابقت داشته باشد
    print("\n--- Starting Log Collector Server ---")
    print("Server URL: http://127.0.0.1:3000/log")
    print("View Logs:  http://127.0.0.1:3000/logs")
    app.run(host='127.0.0.1', port=3000, debug=False)

if __name__ == '__main__':
    run_server()
