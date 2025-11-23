# app.py

import json
from flask import Flask, jsonify, request, Response, g
from business_logic import get_rooms_data, process_add_room, process_booking
import logging
import sqlite3
from typing import Dict, List, Any

# Basic logging configuration (تنظیمات پایه لاگ)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)

# --- Helper for Postman Test Compatibility (تابع کمکی برای سازگاری تست Postman) ---
class CustomJSONEncoder(json.JSONEncoder):
    """Custom encoder to handle sqlite3.Row objects (انكودر سفارشی برای اشیاء sqlite3.Row)"""
    def default(self, obj):
        if isinstance(obj, sqlite3.Row):
            return dict(obj)
        return super().default(obj)

app.json_encoder = CustomJSONEncoder

# --- Database Connection (از آنجایی که logic.py مستقیماً DB را مدیریت می‌کند، این فقط برای Flask best practice است) ---
DB_NAME = 'practise_api.db'

@app.teardown_appcontext
def close_connection(exception):
    """Placeholder for database closing, though models.py manages connections (جایگزین برای بستن دیتابیس)"""
    pass

# --- API Endpoints (نقاط پایانی API) ---

@app.route('/get-room', methods=['GET'])
def get_room():
    """
    Task 1: Retrieves the list of available rooms (Level 0/1 Maturity Model).
    وظیفه ۱: بازیابی لیست اتاق‌های موجود (سطح ۰/۱ مدل بلوغ).
    """
    try:
        rooms_list: List[Dict[str, Any]] = get_rooms_data()
        
        # Server must return code 200 (سرور باید کد ۲۰۰ را برگرداند)
        # The response must contain "rooms" key with the list (پاسخ باید حاوی کلید "rooms" باشد)
        return jsonify({"rooms": rooms_list}), 200
        
    except Exception as e:
        logging.error(f"Error in /get-room: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/add-room', methods=['POST'])
def add_room_endpoint():
    """
    Task 1: Adds a new room based on JSON payload (Level 0/1 Maturity Model).
    وظیفه ۱: افزودن اتاق جدید بر اساس محتوای JSON (سطح ۰/۱ مدل بلوغ).
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    
    try:
        # Add the room and get the new ID (افزودن اتاق و گرفتن ID جدید)
        new_room_id = process_add_room(data)
        
        # After adding, fetch the updated list of rooms (پس از افزودن، لیست به‌روز شده را واکشی کنید)
        rooms_list: List[Dict[str, Any]] = get_rooms_data()
        
        # Server must return code 200 (سرور باید کد ۲۰۰ را برگرداند)
        return jsonify({"rooms": rooms_list}), 200
        
    except ValueError as e:
        logging.warning(f"Validation error in /add-room: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error in /add-room: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/booking', methods=['POST'])
def booking():
    """
    Task 1: Books a room based on roomId in the JSON payload (Level 0/1 Maturity Model).
    وظیفه ۱: رزرو اتاق بر اساس roomId در محتوای JSON (سطح ۰/۱ مدل بلوغ).
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    room_id = data.get('roomId')
    
    if not room_id:
        return jsonify({"error": "roomId is required"}), 400
        
    try:
        room_id = int(room_id)
    except ValueError:
        return jsonify({"error": "roomId must be an integer"}), 400

    try:
        # Attempt to book the room (تلاش برای رزرو اتاق)
        success = process_booking(room_id)
        
        if success:
            # Server must return code 200 (سرور باید کد ۲۰۰ را برگرداند)
            return jsonify({"message": f"Room {room_id} booked successfully"}), 200
        else:
            # Task 1 requirement: Return 409 if the room is already booked or not found (الزام وظیفه ۱: بازگرداندن ۴۰۹)
            return "Произошел конфликт. Комната уже забронирована или не существует.", 409
            
    except Exception as e:
        logging.error(f"Error in /booking: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == '__main__':
    # NOTE: Ensure db_init.py is run once before starting the app (توجه: اطمینان حاصل کنید که db_init.py قبل از شروع برنامه اجرا شده است)
    logging.info("Starting Flask API application...")
    app.run(debug=True, port=5000)
