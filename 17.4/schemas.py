# schemas.py

from marshmallow import Schema, fields, validate, post_load
from typing import Dict, Any
from models import get_author_by_id, create_author

# --- Custom Validator (وظیفه ۲: اعتبارسنجی ID نویسنده) ---

def validate_author_exists(author_id: int):
    """Checks if an Author with the given ID exists in the DB."""
    if get_author_by_id(author_id) is None:
        raise validate.ValidationError(f"Author with ID {author_id} does not exist.")


# --- Author Schemas ---

class AuthorSchema(Schema):
    """Schema for Author creation/retrieval."""
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1))
    last_name = fields.Str(required=True, validate=validate.Length(min=1))
    middle_name = fields.Str(required=False, allow_none=True)

class AuthorBookListSchema(Schema):
    """Schema for displaying a minimal list of books."""
    id = fields.Int(dump_only=True)
    book_name = fields.Str()
    publish_year = fields.Int()
    ISBN = fields.Str()

class AuthorWithBooksSchema(AuthorSchema):
    """Schema for Author details, including a list of their books (وظیفه ۳)."""
    books = fields.List(fields.Nested(AuthorBookListSchema))


# --- Book Schemas ---

class BookSchema(Schema):
    """Base schema for Book serialization/deserialization (for PUT/GET/DELETE)."""
    id = fields.Int(dump_only=True)
    book_name = fields.Str(required=True, validate=validate.Length(min=1))
    publish_year = fields.Int(required=True, validate=validate.Range(min=1800))
    ISBN = fields.Str(required=True, validate=validate.Length(min=10))
    # اعتبارسنجی ID نویسنده: هم اجباری است و هم باید در دیتابیس وجود داشته باشد
    author_id = fields.Int(required=True, validate=validate_author_exists) 

class BookUpdateSchema(Schema):
    """Schema for partial update (PATCH) - all fields are optional."""
    book_name = fields.Str(required=False, validate=validate.Length(min=1))
    publish_year = fields.Int(required=False, validate=validate.Range(min=1800))
    ISBN = fields.Str(required=False, validate=validate.Length(min=10))
    author_id = fields.Int(required=False, validate=validate_author_exists) # اعتبارسنجی وجود نویسنده در صورت ارسال

class BookCreationSchema(BookSchema):
    """Schema for POST /api/books/ - allows nested Author creation (وظیفه ۳)."""
    author = fields.Nested(AuthorSchema, required=False) # فیلد تودرتو برای ایجاد نویسنده جدید

    @post_load
    def process_data(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Handles creating author if nested author data is present."""
        if 'author' in data:
            # اگر داده‌های نویسنده ارائه شده، آن را ایجاد کرده و ID آن را جایگزین می‌کنیم
            author_id = create_author(data['author'])
            data['author_id'] = author_id 
            del data['author']
        
        return data
