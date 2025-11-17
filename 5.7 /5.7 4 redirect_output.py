import sys # Import sys module to access stdout and stderr / ماژول sys را برای دسترسی به stdout و stderr وارد کنید
import io  # Import io module for IOBase type hinting / ماژول io را برای Type Hinting نوع IOBase وارد کنید
import traceback # Import traceback for printing full exception info to stderr / traceback را برای چاپ اطلاعات کامل استثنا در stderr وارد کنید
from typing import Optional # Import Optional for type hinting / Optional را برای Type Hinting وارد کنید

class Redirect:
    """
    A context manager that redirects standard output (sys.stdout) and/or
    standard error (sys.stderr) to specified IO objects (e.g., files).
    Arguments must be keyword-only, allowing redirection of only stdout,
    only stderr, or both.
    
    یک مدیر متن است که خروجی استاندارد (sys.stdout) و/یا
    خطای استاندارد (sys.stderr) را به اشیاء IO مشخص شده (مانند فایل‌ها) تغییر مسیر می‌دهد.
    آرگومان‌ها باید فقط با کلمات کلیدی باشند که امکان تغییر مسیر فقط stdout،
    فقط stderr یا هر دو را فراهم می‌کند.
    """

    def __init__(self, *, stdout: Optional[io.TextIOBase] = None, stderr: Optional[io.TextIOBase] = None):
        """
        Initializes the Redirect context manager.
        
        مدیر متن Redirect را مقداردهی اولیه می‌کند.

        Args:
            stdout (Optional[io.TextIOBase]): An IO object to redirect sys.stdout to. Defaults to None.
                                               یک شیء IO برای تغییر مسیر sys.stdout به آن. پیش‌فرض None است.
            stderr (Optional[io.TextIOBase]): An IO object to redirect sys.stderr to. Defaults to None.
                                               یک شیء IO برای تغییر مسیر sys.stderr به آن. پیش‌فرض None است.
        """
        self._new_stdout = stdout
        self._new_stderr = stderr
        self._old_stdout = None  # To store the original sys.stdout / برای ذخیره sys.stdout اصلی
        self._old_stderr = None  # To store the original sys.stderr / برای ذخیره sys.stderr اصلی

    def __enter__(self):
        """
        Saves the original stdout/stderr streams and redirects them to the new ones.
        
        جریان‌های اصلی stdout/stderr را ذخیره می‌کند و آنها را به جریان‌های جدید تغییر مسیر می‌دهد.
        """
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr

        if self._new_stdout:
            sys.stdout = self._new_stdout
        if self._new_stderr:
            sys.stderr = self._new_stderr

    def __exit__(self, exc_type: Optional[Type[Exception]], exc_val: Optional[Exception], exc_tb: Any) -> bool:
        """
        Restores the original stdout/stderr streams.
        If an exception occurred, it prints the traceback to the (potentially redirected) stderr.
        
        جریان‌های اصلی stdout/stderr را بازیابی می‌کند.
        اگر استثنایی رخ داده باشد، Traceback را به stderr (که احتمالاً تغییر مسیر داده شده است) چاپ می‌کند.

        Args:
            exc_type (Optional[Type[Exception]]): The type of the exception raised.
                                                  نوع استثنای ایجاد شده.
            exc_val (Optional[Exception]): The exception instance.
                                           نمونه استثنا.
            exc_tb (Any): The traceback object.
                          شیء traceback.

        Returns:
            bool: False to re-raise any exception that occurred, True to suppress it.
                  False برای ایجاد مجدد هر استثنایی که رخ داده است، True برای سرکوب آن.
        """
        # Restore original streams regardless of exceptions / جریان‌های اصلی را بدون در نظر گرفتن استثناها بازیابی کنید
        if self._old_stdout:
            sys.stdout = self._old_stdout
        if self._old_stderr:
            sys.stderr = self._old_stderr

        # If an exception occurred within the block, print its traceback to stderr (the current stderr after restoration)
        # اگر استثنایی در داخل بلوک رخ داده است، Traceback آن را به stderr (stderr فعلی پس از بازیابی) چاپ کنید
        if exc_type:
            # We want to print the exception to the *original* stderr (or whatever sys.stderr is now).
            # If the context manager is meant to *redirect* exceptions for logging,
            # this part might need adjustment depending on the exact requirement.
            # The problem example implies that the redirected stderr gets the traceback,
            # and the *original* stdout/stderr gets the 'Hello stdout again' and 'Hello stderr'
            # AFTER the block.
            # بنابراین، این بخش فعلی برای `__exit__` به گونه‌ای عمل می‌کند که استثنا را
            # در جریان `stderr` که در لحظه خروج فعال است، ثبت کند.
            # ما می‌خواهیم استثنا را به *اصلی* stderr (یا هر آنچه که sys.stderr اکنون است) چاپ کنیم.
            # اگر مدیر متن به معنای *تغییر مسیر* استثناها برای گزارش‌گیری باشد،
            # این بخش ممکن است نیاز به تنظیم داشته باشد بسته به نیاز دقیق.
            # مثال مسئله نشان می‌دهد که stderr تغییر مسیر یافته Traceback را دریافت می‌کند،
            # و stdout/stderr *اصلی* 'Hello stdout again' و 'Hello stderr' را
            # پس از بلوک دریافت می‌کند.
            # بنابراین، این بخش فعلی برای `__exit__` به گونه‌ای عمل می‌کند که استثنا را
            # در جریان `stderr` که در لحظه خروج فعال است، ثبت کند.
            # No need to suppress, just let it propagate to be caught by outer handlers or crash.
            # نیازی به سرکوب نیست، فقط اجازه دهید تا توسط کنترل کننده‌های بیرونی گرفته شود یا کرش کند.
            # The example output shows the traceback in `stderr.txt` meaning `sys.stderr` inside `__exit__`
            # still points to `_new_stderr` *before* restoration,
            # or it writes to `_new_stderr` explicitly.
            # خروجی مثال Traceback را در `stderr.txt` نشان می‌دهد به این معنی که `sys.stderr` در داخل `__exit__`
            # همچنان به `_new_stderr` *قبل* از بازیابی اشاره می‌کند،
            # یا به صراحت به `_new_stderr` می‌نویسد.
            
            # To match the example, we print the traceback to the `_new_stderr` *before* restoring it
            # or capture it and write. Let's write to `_new_stderr` if it was set.
            # برای مطابقت با مثال، Traceback را به `_new_stderr` *قبل* از بازیابی آن چاپ می‌کنیم
            # یا آن را ضبط کرده و می‌نویسیم. بیایید به `_new_stderr` بنویسیم اگر تنظیم شده بود.
            if self._new_stderr:
                traceback.print_exception(exc_type, exc_val, exc_tb, file=self._new_stderr)
            else:
                # If only stdout was redirected, or neither, it should go to original stderr
                # اگر فقط stdout تغییر مسیر داده شد، یا هیچ‌کدام، باید به stderr اصلی برود
                traceback.print_exception(exc_type, exc_val, exc_tb, file=self._old_stderr)
            return False # Re-raise the exception / استثنا را دوباره ایجاد کنید
        
        return False # No exception, or exception was handled by us (not the case here) / بدون استثنا، یا استثنا توسط ما مدیریت شد (در اینجا چنین نیست)


# --- Example Usage (as per problem description) ---
if __name__ == '__main__':
    print('Hello stdout (before redirect)')

    # Create dummy files for redirection / فایل‌های ساختگی برای تغییر مسیر ایجاد کنید
    stdout_file = open('stdout.txt', 'w', encoding='utf-8')
    stderr_file = open('stderr.txt', 'w', encoding='utf-8')

    try:
        with Redirect(stdout=stdout_file, stderr=stderr_file):
            print('Hello stdout.txt (inside block)')
            # Simulating an exception that should go to stderr.txt
            # شبیه‌سازی یک استثنا که باید به stderr.txt برود
            raise Exception('Hello stderr.txt (inside block exception)')
    except Exception as e:
        # This catch is for the exception raised inside the block, after it's redirected to stderr.txt
        # این catch برای استثنای ایجاد شده در داخل بلوک است، پس از تغییر مسیر آن به stderr.txt
        # The traceback will be written to stderr.txt by __exit__.
        # The exception itself will propagate out of the with block unless __exit__ returns True.
        # Traceback توسط __exit__ در stderr.txt نوشته خواهد شد.
        # خود استثنا از بلوک with منتقل خواهد شد مگر اینکه __exit__ مقدار True را برگرداند.
        print(f"Caught exception outside Redirect block (after __exit__): {e}", file=sys.stderr)


    print('Hello stdout again (after redirect)')
    
    # Another exception outside the context manager / استثنای دیگری خارج از مدیر متن
    # This should go to the original sys.stderr / این باید به sys.stderr اصلی برود
    raise Exception('Hello stderr (outside redirect exception)')

    # Close the files / فایل‌ها را ببندید
    stdout_file.close()
    stderr_file.close()
