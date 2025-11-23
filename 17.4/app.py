# app.py

from flask import Flask
from flask_restx import Api, Resource, abort
from schemas import (
    BookSchema, BookUpdateSchema, BookCreationSchema, 
    AuthorSchema, AuthorWithBooksSchema
)
from models import (
    get_book_by_id, create_book, update_book, delete_book,
    create_author, delete_author, get_books_by_author_id, get_author_by_id
)
import logging
from marshmallow import ValidationError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)
# فعال‌سازی اعتبارسنجی RESTX (برای اطمینان از اعمال طرح‌ها)
app.config['RESTX_VALIDATE'] = True 

api = Api(
    app, 
    version='1.0', 
    title='Book and Author API',
    description='REST API for managing books and authors.',
    prefix='/api'
)

book_ns = api.namespace('books', description='Book operations')
author_ns = api.namespace('authors', description='Author operations')

# Define Marshmallow Schemas instances
book_schema = BookSchema()
book_update_schema = BookUpdateSchema()
book_creation_schema = BookCreationSchema()
author_schema = AuthorSchema()
author_with_books_schema = AuthorWithBooksSchema()

# --- Helper Functions ---

def handle_validation_error(errors: dict):
    """Aborts with 400 for Marshmallow validation failures."""
    abort(400, message="Validation error.", errors=errors)

# --- Book Resources (وظیفه ۲) ---

@book_ns.route('/<int:book_id>')
class BookResource(Resource):
    """Handles single Book operations: GET, PUT, PATCH, DELETE"""

    def get(self, book_id):
        """GET /api/books/{id} - Get book information"""
        book = get_book_by_id(book_id)
        if not book:
            abort(404, message=f"Book with ID {book_id} not found.")
        
        # استفاده از سریال‌سازی Marshmallow
        return book_schema.dump(book), 200

    def put(self, book_id):
        """PUT /api/books/{id} - Fully update a book"""
        if not get_book_by_id(book_id):
            abort(404, message=f"Book with ID {book_id} not found.")
            
        try:
            # PUT نیاز به تمام فیلدهای طرح پایه دارد
            data = book_schema.load(api.payload) 
        except ValidationError as err:
            handle_validation_error(err.messages)

        if not update_book(book_id, data, partial=False):
            # اگر ISBN تکراری باشد یا خطای دیتابیس رخ دهد
            abort(409, message="ISBN already exists or another DB error occurred.")
            
        return get_book_by_id(book_id), 200

    def patch(self, book_id):
        """PATCH /api/books/{id} - Partially update a book"""
        if not get_book_by_id(book_id):
            abort(404, message=f"Book with ID {book_id} not found.")
            
        try:
            # PATCH از partial=True استفاده می‌کند
            data = book_update_schema.load(api.payload, partial=True) 
        except ValidationError as err:
            handle_validation_error(err.messages)

        if not data:
            abort(400, message="No fields provided for update.")
            
        if not update_book(book_id, data, partial=True):
             abort(409, message="ISBN already exists or another DB error occurred.")
             
        return get_book_by_id(book_id), 200

    def delete(self, book_id):
        """DELETE /api/books/{id} - Delete a book"""
        if delete_book(book_id):
            return '', 204 # 204 No Content
        else:
            abort(404, message=f"Book with ID {book_id} not found.")


@book_ns.route('/')
class BookListResource(Resource):
    """Handles book creation"""
    
    def post(self):
        """POST /api/books/ - Create a new book, allowing nested author creation (وظیفه ۳)"""
        
        try:
            # استفاده از BookCreationSchema برای مدیریت ایجاد نویسنده تودرتو
            data = book_creation_schema.load(api.payload)
        except ValidationError as err:
            handle_validation_error(err.messages)

        book_id = create_book(data)
        
        if book_id is None:
            abort(409, message="A book with this ISBN already exists.")
            
        new_book = get_book_by_id(book_id)
        # استفاده از کد ۲۰۰۱ Created
        return book_schema.dump(new_book), 201 


# --- Author Resources (وظیفه ۳) ---

@author_ns.route('/')
class AuthorListResource(Resource):
    """Handles author creation"""
    
    def post(self):
        """POST /api/authors/ - Create a new author"""
        try:
            data = author_schema.load(api.payload)
        except ValidationError as err:
            handle_validation_error(err.messages)
            
        author_id = create_author(data)
        
        new_author = get_author_by_id(author_id)
        return author_schema.dump(new_author), 201


@author_ns.route('/<int:author_id>')
class AuthorResource(Resource):
    """Handles single Author operations: GET (books list), DELETE"""

    def get(self, author_id):
        """GET /api/authors/{id} - View all books of an author (وظیفه ۳)"""
        author = get_author_by_id(author_id)
        if not author:
            abort(404, message=f"Author with ID {author_id} not found.")
        
        books = get_books_by_author_id(author_id)
        author['books'] = books
        
        # استفاده از طرح تودرتو برای نمایش نویسنده و کتاب‌هایش
        return author_with_books_schema.dump(author), 200

    def delete(self, author_id):
        """DELETE /api/authors/{id} - Delete an author and all their books (وظیفه ۳)"""
        
        if delete_author(author_id):
            # به دلیل ON DELETE CASCADE در DB، کتاب‌ها نیز حذف می‌شوند
            return '', 204 
        else:
            abort(404, message=f"Author with ID {author_id} not found.")


if __name__ == '__main__':
    # توجه: db_init.py را یک بار قبل از شروع برنامه اجرا کنید.
    app.run(debug=True)
