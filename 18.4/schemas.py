# schemas.py
from marshmallow import Schema, fields, validate, post_load
from typing import Dict, Any
from models import get_author_by_id, create_author

def validate_author_exists(author_id: int):
    """Checks if an Author with the given ID exists in the DB."""
    if get_author_by_id(author_id) is None:
        raise validate.ValidationError(f"Author with ID {author_id} does not exist.")

class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1))
    last_name = fields.Str(required=True, validate=validate.Length(min=1))
    middle_name = fields.Str(required=False, allow_none=True)

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    book_name = fields.Str(required=True, validate=validate.Length(min=1))
    publish_year = fields.Int(required=True, validate=validate.Range(min=1800))
    ISBN = fields.Str(required=True, validate=validate.Length(min=10))
    author_id = fields.Int(required=True, validate=validate_author_exists) 

class BookCreationSchema(BookSchema):
    """Allows nested Author creation."""
    author = fields.Nested(AuthorSchema, required=False) 

    @post_load
    def process_data(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Handles creating author if nested author data is present."""
        if 'author' in data:
            author_id = create_author(data['author'])
            data['author_id'] = author_id 
            del data['author']
        
        return data
