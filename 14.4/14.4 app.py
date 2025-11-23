# app.py

import sqlite3
import logging
from flask import Flask, request, render_template, redirect, url_for, g, abort
from forms import BookForm

# Basic logging configuration (تنظیمات پایه لاگ)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)
# IMPORTANT: Set a secret key for Flask-WTF security (مهم: تنظیم کلید مخفی برای امنیت Flask-WTF)
app.config['SECRET_KEY'] = 'your_secret_key_here' 

# Database file name (نام فایل دیتابیس)
DB_NAME = 'practise.db'

# --- Database Connection Management (مدیریت اتصال دیتابیس) ---

def get_db():
    """Returns the database connection (اتصال دیتابیس را برمی‌گرداند)"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_NAME)
        # Configure the connection to return results as dictionaries (ردیف‌ها را به صورت دیکشنری برمی‌گرداند)
        db.row_factory = sqlite3.Row 
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection when the app context ends (اتصال دیتابیس را می‌بندد)"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- Database Interaction Functions (توابع تعامل با دیتابیس) ---

def increment_views_count(cursor: sqlite3.Cursor, book_id: int):
    """Increments the views_count for a specific book (شمارش بازدیدهای یک کتاب را افزایش می‌دهد)"""
    try:
        # Use parametrized query to prevent SQL injection (استفاده از کوئری پارامتری برای جلوگیری از تزریق SQL)
        cursor.execute(
            "UPDATE table_books SET views_count = views_count + 1 WHERE id = ?", 
            (book_id,)
        )
        cursor.connection.commit()
    except sqlite3.Error as e:
        logging.error(f"Error updating views count for book {book_id}: {e}")

# --- Endpoints (مسیرها) ---

@app.route('/books')
def books_list():
    """
    Displays the list of all books and increments their view count (Task 4).
    نمایش لیست همه کتاب‌ها و افزایش شمارش بازدید آنها (وظیفه ۴).
    """
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM table_books ORDER BY id")
        books = cursor.fetchall()

        # Increment views count for all books displayed in the list (Task 4 requirement)
        # افزایش شمارش بازدید برای همه کتاب‌های نمایش داده شده در لیست (الزام وظیفه ۴)
        for book in books:
            increment_views_count(cursor, book['id']) 
            
        return render_template('books.html', books=books)
    
    except sqlite3.Error as e:
        logging.error(f"Database error in books_list: {e}")
        # Return a simple error page/message (بازگشت صفحه/پیام خطای ساده)
        return render_template('base.html', title='Error', content=f"Database Error: {e}")


@app.route('/books/form', methods=['GET', 'POST'])
def add_book_form():
    """
    Handles the book addition form, including validation and DB insertion (Task 1 & 2).
    رسیدگی به فرم افزودن کتاب، از جمله اعتبارسنجی و درج در دیتابیس (وظیفه ۱ و ۲).
    """
    form = BookForm()
    db = get_db()
    cursor = db.cursor()

    # Form validation and submission check (بررسی اعتبارسنجی و ارسال فرم)
    if form.validate_on_submit(): # This handles POST and validation (این POST و اعتبارسنجی را رسیدگی می‌کند)
        try:
            # Task 1: Insert new book into the database
            # وظیفه ۱: درج کتاب جدید در دیتابیس
            cursor.execute(
                """
                INSERT INTO table_books (book_name, author, publish_year, ISBN)
                VALUES (?, ?, ?, ?)
                """,
                (form.book_name.data, form.author.data, form.publish_year.data, form.ISBN.data)
            )
            db.commit()
            logging.info(f"Book '{form.book_name.data}' added successfully.")
            
            # Redirect to the books list to show the new book (Task 1)
            # ریدایرکت به لیست کتاب‌ها برای نمایش کتاب جدید
            return redirect(url_for('books_list'))
            
        except sqlite3.IntegrityError:
            # Handle unique constraint violation (e.g., duplicate ISBN)
            # رسیدگی به نقض محدودیت یکتا بودن (مثلاً ISBN تکراری)
            form.ISBN.errors.append('ISBN уже существует. Пожалуйста, введите уникальный ISBN.')
            return render_template('book_form.html', form=form)
        except sqlite3.Error as e:
            logging.error(f"Database error during insertion: {e}")
            return render_template('base.html', title='Error', content=f"Database Error: {e}")
            
    # Handle GET request or failed POST validation (رسیدگی به درخواست GET یا اعتبارسنجی ناموفق POST)
    return render_template('book_form.html', form=form)


@app.route('/books/author/<string:author_name>')
def author_books(author_name: str):
    """
    Displays all books by a specific author using a template (Task 3).
    نمایش تمام کتاب‌های یک نویسنده خاص با استفاده از یک الگو (وظیفه ۳).
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Use parametrized query (استفاده از کوئری پارامتری)
        cursor.execute(
            "SELECT * FROM table_books WHERE author = ? ORDER BY publish_year DESC", 
            (author_name,)
        )
        books = cursor.fetchall()
        
        # Check if records exist (بررسی وجود رکوردها)
        if not books:
            return render_template('author_books.html', author_name=author_name, books=[], not_found=True)
            
        # Task 3: Render the dedicated template (رندر الگوی اختصاصی)
        return render_template('author_books.html', author_name=author_name, books=books)
    
    except sqlite3.Error as e:
        logging.error(f"Database error in author_books: {e}")
        return render_template('base.html', title='Error', content=f"Database Error: {e}")


@app.route('/books/<int:book_id>')
def book_details(book_id: int):
    """
    Displays details for a single book and increments its view count (Task 4).
    نمایش جزئیات برای یک کتاب واحد و افزایش شمارش بازدید آن (وظیفه ۴).
    """
    db = get_db()
    cursor = db.cursor()

    try:
        # Fetch the book (واکشی کتاب)
        cursor.execute("SELECT * FROM table_books WHERE id = ?", (book_id,))
        book = cursor.fetchone()

        if book is None:
            # Handle case where the book doesn't exist (رسیدگی به موردی که کتاب وجود ندارد)
            # Task requirement: gracefully handle non-existent records
            # الزام وظیفه: رسیدگی درست به رکوردهای غیر موجود
            abort(404, description=f"Книга с ID={book_id} не найдена.") 
            
        # Task 4: Increment views count for this specific book
        # وظیفه ۴: افزایش شمارش بازدید برای این کتاب خاص
        increment_views_count(cursor, book_id)

        # Re-fetch the updated book to show the correct views_count (واکشی مجدد برای نمایش views_count به‌روز شده)
        cursor.execute("SELECT * FROM table_books WHERE id = ?", (book_id,))
        updated_book = cursor.fetchone()

        # Render the template (رندر الگو)
        return render_template('book_details.html', book=updated_book)

    except sqlite3.Error as e:
        logging.error(f"Database error in book_details: {e}")
        return render_template('base.html', title='Error', content=f"Database Error: {e}")


if __name__ == '__main__':
    # NOTE: Run db_init.py once before starting the app (توجه: db_init.py را یک بار قبل از شروع برنامه اجرا کنید)
    logging.info("Starting Flask application...")
    app.run(debug=True)
