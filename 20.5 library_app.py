# library_app.py

from datetime import datetime, timedelta
from typing import List
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Session
from sqlalchemy import func

# --- 1. تنظیمات پایگاه داده و ORM ---

DATABASE_URL = "sqlite:///library.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- 2. تعریف مدل‌های ORM ---

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False) # بدون ForeignKey در این مرحله

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    # --- Classmethods درخواستی ---

    @classmethod
    def get_scholarship_students(cls, session: Session) -> List['Student']:
        """دریافت لیست دانشجویانی که دارای بورسیه هستند."""
        return session.query(cls).filter(cls.scholarship == True).all()

    @classmethod
    def get_students_by_score(cls, session: Session, min_score: float) -> List['Student']:
        """دریافت لیست دانشجویانی که میانگین نمره‌شان بالاتر از min_score است."""
        return session.query(cls).filter(cls.average_score > min_score).all()

class ReceivingBook(Base):
    __tablename__ = 'receiving_books'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False) # بدون ForeignKey در این مرحله
    student_id = Column(Integer, nullable=False) # بدون ForeignKey در این مرحله
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime, default=None, nullable=True)

    # --- Hybrid Property درخواستی: count_date_with_book ---

    @hybrid_property
    def count_date_with_book(self) -> int:
        """تعداد روزهایی که کتاب نزد خواننده بوده/هست."""
        end_date = self.date_of_return if self.date_of_return else datetime.now()
        if self.date_of_issue:
            diff = end_date - self.date_of_issue
            return diff.days
        return 0

    @count_date_with_book.expression
    def count_date_with_book(cls):
        """نسخه Expression برای استفاده در کوئری‌های SQL (فیلتر کردن و مرتب‌سازی)."""
        return func.julianday(func.coalesce(cls.date_of_return, func.datetime('now'))) - func.julianday(cls.date_of_issue)

# ایجاد جداول
Base.metadata.create_all(bind=engine)

# --- 3. تنظیمات Flask و رووت‌ها ---

app = Flask(__name__)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

# --- رووت ۱: دریافت همه کتاب‌ها (GET) ---
@app.route('/books', methods=['GET'])
def get_all_books():
    db = get_db()
    all_books = db.query(Book).all()
    books_data = [{
        'id': book.id, 'name': book.name, 'count': book.count, 
        'release_date': str(book.release_date), 'author_id': book.author_id
    } for book in all_books]
    return jsonify(books_data)

# --- رووت ۲: دریافت لیست بدهکاران (GET) ---
@app.route('/debtors', methods=['GET'])
def get_debtors():
    db = get_db()
    fourteen_days_ago = datetime.now() - timedelta(days=14)
    
    # بدهکاران: کتاب‌هایی که برگردانده نشده‌اند (None) و تاریخ صدور آن‌ها بیش از 14 روز پیش است
    debtors_records = db.query(ReceivingBook).filter(
        ReceivingBook.date_of_return == None,
        ReceivingBook.date_of_issue < fourteen_days_ago
    ).all()
    
    debtors_list = [{
        'receiving_id': record.id, 'student_id': record.student_id,
        'book_id': record.book_id, 'issue_date': str(record.date_of_issue),
        'days_overdue': record.count_date_with_book
    } for record in debtors_records]
    
    return jsonify(debtors_list)

# --- رووت ۳: выдача کتاب به دانشجو (POST) ---
@app.route('/issue_book', methods=['POST'])
def issue_book():
    data = request.get_json()
    book_id = data.get('book_id')
    student_id = data.get('student_id')
    
    if not book_id or not student_id:
        return jsonify({'error': 'Missing book_id or student_id'}), 400

    db = get_db()
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book or book.count < 1:
        return jsonify({'error': f'Book ID {book_id} not found or count is 0.'}), 404

    new_issue = ReceivingBook(
        book_id=book_id, student_id=student_id, date_of_issue=datetime.now()
    )
    book.count -= 1

    try:
        db.add(new_issue)
        db.commit()
        return jsonify({'message': f'Book ID {book_id} successfully issued to Student ID {student_id}.'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

# --- رووت ۴: سابقه کتاب (POST) ---
@app.route('/return_book', methods=['POST'])
def return_book():
    data = request.get_json()
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    if not book_id or not student_id:
        return jsonify({'error': 'Missing book_id or student_id'}), 400

    db = get_db()
    issue_record = db.query(ReceivingBook).filter(
        ReceivingBook.book_id == book_id,
        ReceivingBook.student_id == student_id,
        ReceivingBook.date_of_return == None
    ).first()

    if not issue_record:
        return jsonify({'error': 'No active issue record found for this book/student combination.'}), 404

    issue_record.date_of_return = datetime.now()
    
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        book.count += 1
    
    try:
        db.commit()
        return jsonify({'message': f'Book ID {book_id} successfully returned by Student ID {student_id}. Days held: {issue_record.count_date_with_book}'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

# --- رووت ۵ (اختیاری): جستجوی کتاب بر اساس عنوان (GET) ---
@app.route('/books/search', methods=['GET'])
def search_books():
    search_term = request.args.get('q') 
    
    if not search_term:
        return jsonify({'error': 'Please provide a search term using the "q" parameter.'}), 400

    db = get_db()
    
    # استفاده از .ilike() برای جستجوی رشته‌ای غیرحساس به حروف
    matching_books = db.query(Book).filter(Book.name.ilike(f'%{search_term}%')).all()
    
    books_data = [{
        'id': book.id, 'name': book.name, 'release_date': str(book.release_date)
    } for book in matching_books]
    
    if not books_data:
        return jsonify({'message': 'No books found matching the search term.'}), 404
    
    return jsonify(books_data)

if __name__ == '__main__':
    # این بخش برای پر کردن اولیه دیتابیس است (برای تست)
    db = SessionLocal()
    if db.query(Book).count() == 0:
        db.add_all([
            Author(name='فردریش', surname='نیچه'), Author(name='جورج', surname='اورول'),
            Book(name='چنین گفت زرتشت', count=5, release_date=datetime(1883, 1, 1).date(), author_id=1),
            Book(name='1984', count=2, release_date=datetime(1949, 1, 1).date(), author_id=2),
            Student(name='علی', surname='احمدی', phone='111', email='a@a.com', average_score=4.5, scholarship=True),
            Student(name='سارا', surname='محمدی', phone='222', email='b@b.com', average_score=3.2, scholarship=False),
            # رکورد بدهکار برای تست
            ReceivingBook(book_id=1, student_id=2, date_of_issue=datetime.now() - timedelta(days=20), date_of_return=None) 
        ])
        db.commit()
    db.close()
    
    app.run(debug=True)
