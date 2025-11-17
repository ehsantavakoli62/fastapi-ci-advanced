import pytest
import sys
import io
import os
import traceback
from redirect_output import Redirect # Import the context manager / مدیر متن را وارد کنید

# Fixture to create temporary files for testing / Fixture برای ایجاد فایل‌های موقت برای آزمایش
@pytest.fixture
def temp_files():
    """Creates temporary files for stdout/stderr redirection and cleans them up."""
    """فایل‌های موقت برای stdout/stderr redirection ایجاد می‌کند و آنها را پاک می‌کند."""
    stdout_fname = "test_stdout.txt"
    stderr_fname = "test_stderr.txt"
    
    # Ensure files don't exist from previous failed runs / اطمینان حاصل کنید که فایل‌ها از اجراهای ناموفق قبلی وجود ندارند
    if os.path.exists(stdout_fname):
        os.remove(stdout_fname)
    if os.path.exists(stderr_fname):
        os.remove(stderr_fname)

    stdout_file = open(stdout_fname, 'w', encoding='utf-8')
    stderr_file = open(stderr_fname, 'w', encoding='utf-8')
    
    yield stdout_file, stderr_file, stdout_fname, stderr_fname
    
    stdout_file.close()
    stderr_file.close()
    
    if os.path.exists(stdout_fname):
        os.remove(stdout_fname)
    if os.path.exists(stderr_fname):
        os.remove(stderr_fname)

def test_redirect_both_stdout_and_stderr(temp_files):
    """
    Test case: Both stdout and stderr are redirected to files.
    مورد تست: هر دو stdout و stderr به فایل‌ها تغییر مسیر داده می‌شوند.
    """
    stdout_file, stderr_file, stdout_fname, stderr_fname = temp_files
    
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    with Redirect(stdout=stdout_file, stderr=stderr_file):
        print("Hello from redirected stdout")
        sys.stderr.write("Hello from redirected stderr\n")
    
    # Ensure streams are restored / اطمینان حاصل کنید که جریان‌ها بازیابی شده‌اند
    assert sys.stdout is original_stdout
    assert sys.stderr is original_stderr
    
    # Check file content / محتوای فایل را بررسی کنید
    stdout_file.close() # Close to ensure content is flushed / برای اطمینان از فلاش شدن محتوا ببندید
    stderr_file.close()
    
    with open(stdout_fname, 'r', encoding='utf-8') as f:
        assert f.read().strip() == "Hello from redirected stdout"
    with open(stderr_fname, 'r', encoding='utf-8') as f:
        assert f.read().strip() == "Hello from redirected stderr"

def test_redirect_only_stdout(temp_files):
    """
    Test case: Only stdout is redirected, stderr should remain unchanged.
    مورد تست: فقط stdout تغییر مسیر داده می‌شود، stderr باید بدون تغییر باقی بماند.
    """
    stdout_file, _, stdout_fname, _ = temp_files
    
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    # Use a StringIO to capture original stderr output for verification / از StringIO برای گرفتن خروجی stderr اصلی برای تأیید استفاده کنید
    # This is a common pattern when you expect something to go to the actual console stderr.
    # این یک الگوی رایج است وقتی انتظار دارید چیزی به stderr کنسول واقعی برود.
    captured_stderr = io.StringIO()
    sys.stderr = captured_stderr

    try:
        with Redirect(stdout=stdout_file):
            print("Hello stdout only")
            sys.stderr.write("Hello original stderr\n") # This should go to `captured_stderr` / این باید به `captured_stderr` برود
        
        # Ensure streams are restored / اطمینان حاصل کنید که جریان‌ها بازیابی شده‌اند
        assert sys.stdout is original_stdout
        # Assert that the stderr was restored, though we've manually captured it.
        # تأیید کنید که stderr بازیابی شده است، اگرچه ما آن را به صورت دستی گرفته‌ایم.
        # This means `sys.stderr` should point back to whatever it was before `sys.stderr = captured_stderr`.
        # این به این معنی است که `sys.stderr` باید به هر آنچه قبل از `sys.stderr = captured_stderr` بود، اشاره کند.
        # For this test, we *temporarily* changed `sys.stderr` to `captured_stderr` to check output.
        # برای این تست، ما *موقت* `sys.stderr` را به `captured_stderr` تغییر دادیم تا خروجی را بررسی کنیم.
        # The `Redirect` context manager should restore `sys.stderr` to `captured_stderr` if it wasn't
        # redirected by `Redirect` itself.
        # مدیر متن `Redirect` باید `sys.stderr` را به `captured_stderr` بازیابی کند اگر توسط خود `Redirect`
        # تغییر مسیر داده نشد.
        assert sys.stderr is captured_stderr # It should still be our captured stream / باید هنوز جریان گرفته شده ما باشد

        # Check file content / محتوای فایل را بررسی کنید
        stdout_file.close()
        with open(stdout_fname, 'r', encoding='utf-8') as f:
            assert f.read().strip() == "Hello stdout only"
        
        # Check captured stderr content / محتوای stderr گرفته شده را بررسی کنید
        assert captured_stderr.getvalue().strip() == "Hello original stderr"

    finally:
        sys.stderr = original_stderr # Restore the actual original stderr / stderr اصلی واقعی را بازیابی کنید


def test_redirect_only_stderr(temp_files):
    """
    Test case: Only stderr is redirected, stdout should remain unchanged.
    مورد تست: فقط stderr تغییر مسیر داده می‌شود، stdout باید بدون تغییر باقی بماند.
    """
    _, stderr_file, _, stderr_fname = temp_files
    
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    captured_stdout = io.StringIO()
    sys.stdout = captured_stdout

    try:
        with Redirect(stderr=stderr_file):
            print("Hello original stdout") # This should go to `captured_stdout` / این باید به `captured_stdout` برود
            sys.stderr.write("Hello stderr only\n")
        
        # Ensure streams are restored / اطمینان حاصل کنید که جریان‌ها بازیابی شده‌اند
        assert sys.stdout is captured_stdout # It should still be our captured stream / باید هنوز جریان گرفته شده ما باشد
        assert sys.stderr is original_stderr
        
        # Check file content / محتوای فایل را بررسی کنید
        stderr_file.close()
        with open(stderr_fname, 'r', encoding='utf-8') as f:
            assert f.read().strip() == "Hello stderr only"
        
        # Check captured stdout content / محتوای stdout گرفته شده را بررسی کنید
        assert captured_stdout.getvalue().strip() == "Hello original stdout"
        
    finally:
        sys.stdout = original_stdout # Restore the actual original stdout / stdout اصلی واقعی را بازیابی کنید

def test_no_arguments_no_redirection(temp_files):
    """
    Test case: Context manager used without arguments, no redirection should occur.
    مورد تست: مدیر متن بدون آرگومان استفاده می‌شود، نباید هیچ تغییر مسیری رخ دهد.
    """
    stdout_file, stderr_file, stdout_fname, stderr_fname = temp_files
    
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    # Capture outputs to verify nothing was redirected by Redirect itself / خروجی‌ها را بگیرید تا تأیید کنید هیچ چیز توسط خود Redirect تغییر مسیر داده نشد
    captured_stdout = io.StringIO()
    captured_stderr = io.StringIO()
    sys.stdout = captured_stdout
    sys.stderr = captured_stderr

    try:
        with Redirect():
            print("Hello normal stdout")
            sys.stderr.write("Hello normal stderr\n")
        
        # Streams should remain as captured streams / جریان‌ها باید به عنوان جریان‌های گرفته شده باقی بمانند
        assert sys.stdout is captured_stdout
        assert sys.stderr is captured_stderr
        
        assert captured_stdout.getvalue().strip() == "Hello normal stdout"
        assert captured_stderr.getvalue().strip() == "Hello normal stderr"

        # The files should be empty as nothing was redirected to them / فایل‌ها باید خالی باشند زیرا هیچ چیز به آنها تغییر مسیر داده نشد
        stdout_file.close()
        stderr_file.close()
        with open(stdout_fname, 'r', encoding='utf-8') as f:
            assert f.read().strip() == ""
        with open(stderr_fname, 'r', encoding='utf-8') as f:
            assert f.read().strip() == ""

    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr


def test_exception_redirection_to_stderr_file(temp_files):
    """
    Test case: An exception raised inside the block should have its traceback
    written to the redirected stderr file.
    مورد تست: یک استثنا که در داخل بلوک ایجاد می‌شود، باید Traceback آن
    در فایل stderr تغییر مسیر داده شده نوشته شود.
    """
    stdout_file, stderr_file, stdout_fname, stderr_fname = temp_files
    
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    try:
        with Redirect(stdout=stdout_file, stderr=stderr_file):
            print("Output before exception")
            raise ValueError("Test exception for stderr redirection")
        pytest.fail("Exception was not propagated.") # Should not be reached / نباید به اینجا برسیم
    except ValueError as e:
        assert str(e) == "Test exception for stderr redirection"
        # The exception itself is re-raised and caught here / خود استثنا دوباره ایجاد شده و اینجا گرفته می‌شود
    
    # Ensure streams are restored / اطمینان حاصل کنید که جریان‌ها بازیابی شده‌اند
    assert sys.stdout is original_stdout
    assert sys.stderr is original_stderr
    
    stdout_file.close()
    stderr_file.close()

    with open(stdout_fname, 'r', encoding='utf-8') as f:
        assert f.read().strip() == "Output before exception"
    
    with open(stderr_fname, 'r', encoding='utf-8') as f:
        stderr_content = f.read()
        assert "Traceback (most recent call last):" in stderr_content
        assert "ValueError: Test exception for stderr redirection" in stderr_content

def test_nested_redirects(temp_files):
    """
    Test case: Nested Redirect context managers should handle streams correctly.
    مورد تست: مدیران متن Redirect تو در تو باید جریان‌ها را به درستی مدیریت کنند.
    """
    outer_stdout_f, outer_stderr_f, outer_stdout_fname, outer_stderr_fname = temp_files
    
    # Create another set of files for the inner redirect / مجموعه دیگری از فایل‌ها برای تغییر مسیر داخلی ایجاد کنید
    inner_stdout_fname = "test_inner_stdout.txt"
    inner_stderr_fname = "test_inner_stderr.txt"
    inner_stdout_f = open(inner_stdout_fname, 'w', encoding='utf-8')
    inner_stderr_f = open(inner_stderr_fname, 'w', encoding='utf-8')

    original_stdout = sys.stdout
    original_stderr = sys.stderr

    try:
        with Redirect(stdout=outer_stdout_f, stderr=outer_stderr_f):
            print("Outer stdout 1")
            sys.stderr.write("Outer stderr 1\n")

            with Redirect(stdout=inner_stdout_f, stderr=inner_stderr_f):
                print("Inner stdout")
                sys.stderr.write("Inner stderr\n")
                raise RuntimeError("Exception from inner block")
            
            # This print/stderr.write will go to outer files again
            # این print/stderr.write دوباره به فایل‌های بیرونی می‌رود
            print("Outer stdout 2 (after inner block)")
            sys.stderr.write("Outer stderr 2 (after inner block)\n")
            
    except RuntimeError as e:
        assert str(e) == "Exception from inner block"
    
    finally:
        inner_stdout_f.close()
        inner_stderr_f.close()
        if os.path.exists(inner_stdout_fname): os.remove(inner_stdout_fname)
        if os.path.exists(inner_stderr_fname): os.remove(inner_stderr_fname)

    # Check outer files / فایل‌های بیرونی را بررسی کنید
    outer_stdout_f.close()
    outer_stderr_f.close()

    with open(outer_stdout_fname, 'r', encoding='utf-8') as f:
        outer_stdout_content = f.read().strip()
        assert "Outer stdout 1" in outer_stdout_content
        assert "Outer stdout 2 (after inner block)" in outer_stdout_content
        assert "Inner stdout" not in outer_stdout_content # Inner output should not be here / خروجی داخلی نباید اینجا باشد

    with open(outer_stderr_fname, 'r', encoding='utf-8') as f:
        outer_stderr_content = f.read()
        assert "Outer stderr 1" in outer_stderr_content
        assert "Outer stderr 2 (after inner block)" in outer_stderr_content
        assert "Inner stderr" not in outer_stderr_content # Inner error should not be here / خطای داخلی نباید اینجا باشد
        assert "Traceback (most recent call last):" in outer_stderr_content # Inner exception goes to outer stderr / استثنای داخلی به stderr بیرونی می‌رود
        assert "RuntimeError: Exception from inner block" in outer_stderr_content

    # Check inner files / فایل‌های داخلی را بررسی کنید
    with open(inner_stdout_fname, 'r', encoding='utf-8') as f:
        assert f.read().strip() == "Inner stdout"
    with open(inner_stderr_fname, 'r', encoding='utf-8') as f:
        assert f.read().strip() == "Inner stderr"
        # The exception traceback is NOT in the inner stderr.txt, but propagated to the outer.
        # This is due to `__exit__` in the inner Redirect printing to `sys.stderr` *at that moment*,
        # which is the outer redirected `stderr_file`.
        # Traceback استثنا در inner stderr.txt نیست، بلکه به بیرونی منتقل شده است.
        # این به دلیل `__exit__` در Redirect داخلی است که در آن لحظه به `sys.stderr` چاپ می‌کند،
        # که همان `stderr_file` تغییر مسیر یافته بیرونی است.
        # The problem statement example has the traceback going to the *redirected* stderr,
        # which implies that the `__exit__` of the inner block should print to its `_new_stderr`.
        # This is handled by the explicit `if self._new_stderr:` check in `__exit__`.
        # مثال صورت مسئله Traceback را به stderr *تغییر مسیر داده شده* می‌فرستد،
        # که به این معنی است که `__exit__` بلوک داخلی باید به `_new_stderr` خود چاپ کند.
        # این توسط بررسی صریح `if self._new_stderr:` در `__exit__` مدیریت می‌شود.
