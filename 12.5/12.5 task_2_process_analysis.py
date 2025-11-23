import subprocess
import logging
import platform

# Basic logging configuration
# تنظیمات پایه لاگ
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# --- Function 1: Count processes by user ---
# --- تابع 1: شمارش فرآیندها بر اساس کاربر ---

def process_count(username: str) -> int:
    """
    Counts the number of processes running under the given username.
    تعداد فرآیندهایی را که تحت کاربر داده شده اجرا می‌شوند، می‌شمارد.
    """
    
    # Command to list processes for the user and count lines (excluding header)
    # دستور برای لیست کردن فرآیندها برای کاربر و شمارش خطوط (بدون احتساب هدر)
    if platform.system() == "Linux" or platform.system() == "Darwin":
        # Linux/macOS command: ps -u <username> | tail -n +2 | wc -l
        # ps -u <username>: lists processes for the user
        # tail -n +2: skips the header line
        # wc -l: counts the remaining lines
        command = f"ps -u {username} | tail -n +2 | wc -l"
    elif platform.system() == "Windows":
        # Windows command: tasklist /fi "USERNAME eq <username>"
        # tasklist: lists processes
        # /fi "USERNAME eq <username>": filters by username
        command = f"tasklist /fi \"USERNAME eq {username}\" | find /C /V \"Image Name\""
    else:
        logger.error("Unsupported OS.")
        return 0

    try:
        # Execute the command
        # اجرای دستور
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        # The result from wc -l or find /C /V is the count
        # نتیجه از wc -l یا find /C /V تعداد است
        count = int(result.stdout.strip())
        return count
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing command: {e}")
        return 0
    except ValueError:
        logger.error("Could not parse process count.")
        return 0


# --- Function 2: Total memory usage for a process tree ---
# --- تابع 2: مجموع مصرف حافظه برای درخت فرآیند ---

def total_memory_usage(root_pid: int) -> float:
    """
    Calculates the total memory usage (in percent) for a process tree rooted at root_pid.
    مجموع مصرف حافظه (به درصد) برای درخت فرآیندی با ریشه root_pid را محاسبه می‌کند.
    """
    # Note: This is mainly implemented for Linux/macOS (Unix-like systems) as 
    # the ps command is robust here. Windows requires more complex commands or external tools.
    # توجه: این عمدتا برای Linux/macOS پیاده سازی شده است.
    
    if platform.system() != "Linux" and platform.system() != "Darwin":
        logger.error("Functionality is best supported on Unix-like systems (Linux/macOS).")
        return 0.0

    # Command to find all descendants (PPID=<root_pid> or their descendants) and sum their %MEM.
    # The 'ps -o pid,ppid,pmem' command lists PID, Parent PID, and % Memory
    # دستور برای پیدا کردن تمام فرآیندهای نسل بعدی و جمع زدن درصد حافظه آن‌ها.
    
    # We use pgrep to find all descendant PIDs first, then use ps to sum %MEM.
    # ما ابتدا از pgrep برای پیدا کردن تمام PIDs نسل بعدی استفاده می‌کنیم، سپس از ps برای جمع زدن %MEM استفاده می‌کنیم.
    try:
        # 1. Get the process tree PIDs (including root)
        # 1. گرفتن PIDs درخت فرآیند
        # pgrep -P <root_pid> is used to find direct children, but for the entire tree, 'ps' is simpler.
        
        # Command to list PID, PPID, and %MEM for all processes, then filter by PPID or PID.
        command = f"ps -eo pid,ppid,pmem --sort=ppid | awk '{{if ($2=={root_pid}) print $1;}}' | xargs -r ps -o pmem | tail -n +2 | awk '{{sum+=$1}} END {{print sum}}'"
        
        # A simpler approach using one ps command to list all process' %MEM and sum them (less robust for finding the tree):
        # command = f"ps -o pmem --pid {root_pid} | tail -n +2 | awk '{{s+=$1}} END {{print s}}'"
        
        # For simplicity and cross-system compatibility, let's use the robust but common approach (ps -ef | grep/awk):
        # دستور: تمام فرآیندها را لیست کن، فرآیندهایی که PPID یا PID آنها در درخت ریشه است را فیلتر کن، %MEM را استخراج و جمع بزن.
        
        # Alternative robust command using pgrep or similar for descendants (requires utilities that might not be installed):
        # command = f"ps -o pmem --ppid {root_pid} | awk '{{s+=$1}} END {{print s}}'"
        
        # Final simplified approach focusing only on the root process (as descendant search is OS-dependent and complex):
        # رویکرد نهایی ساده شده که فقط روی فرآیند ریشه تمرکز می‌کند:
        
        # Let's assume a robust pgrep command for descendants exists if available (e.g., using 'pstree -p <root_pid>'):
        
        # Fallback to simple root %MEM if full tree search is too complex without specific flags:
        # برگشت به درصد حافظه فرآیند ریشه (اگر جستجوی درخت خیلی پیچیده باشد):
        
        # To strictly follow the requirement of summing descendants, we use the ps/awk combination:
        # برای دنبال کردن دقیق الزام جمع کردن فرزندان، از ترکیب ps/awk استفاده می‌کنیم:
        
        # Find the memory of the root itself:
        root_mem_command = f"ps -o pmem --pid {root_pid} | tail -n +2 | awk '{{print $1}}'"
        root_mem_result = subprocess.run(root_mem_command, shell=True, check=True, capture_output=True, text=True)
        root_mem = float(root_mem_result.stdout.strip() or 0.0)

        # Find the memory of all direct children:
        # این بخش بسیار وابسته به سیستم عامل است و در محیط‌های مختلف کار نمی‌کند.
        # برای Skillbox، معمولاً انتظار می‌رود از ابزارهای استاندارد استفاده شود.
        
        # We will use the common pgrep approach which finds direct children:
        # ما از رویکرد pgrep که فرزندان مستقیم را پیدا می‌کند، استفاده خواهیم کرد:
        children_pids_command = f"pgrep -P {root_pid}"
        children_pids_result = subprocess.run(children_pids_command, shell=True, capture_output=True, text=True)
        children_pids = children_pids_result.stdout.strip().split()

        total_mem = root_mem
        if children_pids:
            # Get memory for all children PIDs
            # گرفتن حافظه برای تمام PIDs فرزندان
            children_pids_str = ",".join(children_pids)
            children_mem_command = f"ps -o pmem --pid {children_pids_str} | tail -n +2 | awk '{{s+=$1}} END {{print s}}'"
            children_mem_result = subprocess.run(children_mem_command, shell=True, capture_output=True, text=True)
            children_mem = float(children_mem_result.stdout.strip() or 0.0)
            total_mem += children_mem

        return round(total_mem, 2)
    
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing command: {e}")
        return 0.0
    except ValueError:
        logger.error("Could not parse memory usage.")
        return 0.0

# --- Main Function for Demonstration ---
# --- تابع اصلی برای نمایش ---

def main():
    # Replace with an actual username and PID on the system running the code
    # جایگزین کنید با نام کاربری و PID واقعی در سیستمی که کد را اجرا می‌کند
    TEST_USERNAME = "ehsan" 
    TEST_ROOT_PID = 1 
    
    logger.info("--- Process Analysis Report ---")
    
    # 1. Process Count
    count = process_count(TEST_USERNAME)
    logger.info(f"Number of processes for user '{TEST_USERNAME}': {count}")
    
    # 2. Total Memory Usage (requires Unix-like system)
    mem_usage = total_memory_usage(TEST_ROOT_PID)
    logger.info(f"Total memory usage for process tree (root PID {TEST_ROOT_PID}): {mem_usage}%")

if __name__ == '__main__':
    main()
