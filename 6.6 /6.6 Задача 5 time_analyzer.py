import logging
import subprocess
import re
from datetime import datetime
import os
import sys

# --- Configuration ---
LOG_FILE_FOR_MEASUREMENT = 'measure_me_logs.log'
MEASURE_ME_SCRIPT = 'measure_me.py'

def run_and_capture_logs():
    """
    Runs the measure_me.py script as a subprocess and captures its stdout to a log file.
    
    اسکریپت measure_me.py را به عنوان یک زیرپروسس اجرا می‌کند و خروجی stdout آن را در یک فایل لاگ ثبت می‌کند.
    """
    if not os.path.exists(MEASURE_ME_SCRIPT):
        print(f"Error: Script '{MEASURE_ME_SCRIPT}' not found in the current directory.", file=sys.stderr)
        return False

    with open(LOG_FILE_FOR_MEASUREMENT, 'w', encoding='utf-8') as log_file_handle:
        try:
            subprocess.run(
                [sys.executable, MEASURE_ME_SCRIPT], 
                stdout=log_file_handle, 
                stderr=subprocess.PIPE, 
                text=True, 
                check=True 
            )
        except subprocess.CalledProcessError as e:
            print(f"Error running '{MEASURE_ME_SCRIPT}': {e}", file=sys.stderr)
            print(f"Stderr: {e.stderr}", file=sys.stderr)
            return False
        except FileNotFoundError:
            print(f"Error: Python interpreter '{sys.executable}' not found.", file=sys.stderr)
            return False
    return True

def analyze_measurement_logs() -> float:
    """
    Analyzes the log file to calculate the average execution time of measure_me.
    Assumes log format: 'YYYY-MM-DD HH:MM:SS,ms - Message'
    
    فایل لاگ را برای محاسبه میانگین زمان اجرای measure_me تجزیه و تحلیل می‌کند.
    فرمت لاگ فرض می‌شود: 'YYYY-MM-DD HH:MM:SS,ms - Message'

    Returns:
        float: The average execution time in seconds, or -1 if no data.
               میانگین زمان اجرا بر حسب ثانیه، یا -1 اگر داده‌ای وجود نداشته باشد.
    """
    execution_times = []
    enter_times = {}

    try:
        with open(LOG_FILE_FOR_MEASUREMENT, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),(\d{3}) - (.*)', line)
                if match:
                    timestamp_part, msecs_part, message = match.groups()
                    timestamp = datetime.strptime(f"{timestamp_part}.{msecs_part}", '%Y-%m-%d %H:%M:%S.%f')
                    
                    if "Enter measure_me" in message:
                        run_id = len(enter_times)
                        enter_times[run_id] = timestamp
                    elif "Leave measure_me" in message:
                        if enter_times:
                            run_id = max(enter_times.keys())
                            entry_time = enter_times.pop(run_id)
                            
                            duration = (timestamp - entry_time).total_seconds()
                            execution_times.append(duration)

    except FileNotFoundError:
        print(f"Error: Log file '{LOG_FILE_FOR_MEASUREMENT}' not found for analysis.", file=sys.stderr)
        return -1.0
    except Exception as e:
        print(f"Error analyzing log file: {e}", file=sys.stderr)
        return -1.0

    if execution_times:
        average_time = sum(execution_times) / len(execution_times)
        return average_time
    else:
        return -1.0
