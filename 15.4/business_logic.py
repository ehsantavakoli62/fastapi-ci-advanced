# business_logic.py

from models import get_all_available_rooms, add_room, book_room_by_id, get_room_status_by_id
from typing import List, Dict, Any, Optional

def get_rooms_data() -> List[Dict[str, Any]]:
    """Fetches all available rooms (بازیابی تمام اتاق‌های موجود)"""
    return get_all_available_rooms()

def process_add_room(data: Dict[str, Any]) -> int:
    """Processes room addition request (پردازش درخواست افزودن اتاق)"""
    # Simple validation for demonstration: ensuring required fields are present
    # اعتبارسنجی ساده برای نمایش: اطمینان از وجود فیلدهای مورد نیاز
    required_fields = ['floor', 'guestNum', 'beds', 'price']
    if not all(field in data for field in required_fields):
        raise ValueError("Missing required room fields.")
        
    # Ensure numerical types (اطمینان از انواع عددی)
    room_data = {k: int(data[k]) for k in required_fields}
    
    return add_room(room_data)

def process_booking(room_id: int) -> bool:
    """Handles the booking process (رسیدگی به فرآیند رزرو)"""
    # Check if the room is already booked before attempting to book (بررسی وضعیت رزرو قبل از اقدام)
    status = get_room_status_by_id(room_id)
    
    if status is None:
        # Room does not exist (اتاق وجود ندارد)
        return False
    
    if status == 0:
        # Already booked (از قبل رزرو شده است)
        return False
        
    # Attempt to book (اقدام به رزرو)
    return book_room_by_id(room_id)
