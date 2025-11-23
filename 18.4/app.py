# app.py

import logging
from flask import Flask
from flask_restx import Api, Resource, abort
from flasgger import Swagger, swag_from # وظیفه ۱
from flask_jsonrpc import JSONRPC # وظیفه ۳
from werkzeug.serving import WSGIRequestHandler # وظیفه ۲

from schemas import BookCreationSchema, AuthorSchema
from models import create_book, get_book_by_id, create_author

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)
app.config['RESTX_VALIDATE'] = True 

# --- Setup for 18.4 ---
Swagger(app) # Flasgger for Documentation (Task 1)
jsonrpc = JSONRPC(app, '/api/rpc', enable_web_browsing=True) # JSON-RPC (Task 3)

api = Api(
    app, 
    version='1.0', 
    title='Book and Author API',
    description='REST API for managing books and authors.',
    prefix='/api'
)

book_ns = api.namespace('books', description='Book operations')
author_ns = api.namespace('authors', description='Author operations')

book_creation_schema = BookCreationSchema()
author_schema = AuthorSchema()

def handle_validation_error(errors: dict):
    abort(400, message="Validation error.", errors=errors)

# --- REST Resources ---

@book_ns.route('/')
class BookListResource(Resource):
    
    @swag_from('./docs/book_post.yml') # وظیفه ۱: استفاده از YAML
    def post(self):
        try:
            data = book_creation_schema.load(api.payload)
        except Exception as err:
            handle_validation_error(err.messages)

        book_id = create_book(data)
        
        if book_id is None:
            abort(409, message="A book with this ISBN already exists.")
            
        new_book = get_book_by_id(book_id)
        return new_book, 201 

@author_ns.route('/')
class AuthorListResource(Resource):
    
    @swag_from('./docs/author_post.json') # وظیفه ۱: استفاده از JSON
    def post(self):
        try:
            data = author_schema.load(api.payload)
        except Exception as err:
            handle_validation_error(err.messages)
            
        author_id = create_author(data)
        
        new_author = get_author_by_id(author_id)
        return new_author, 201

# --- JSON-RPC Methods (Task 3) ---

@jsonrpc.method('Math.add(a=Number, b=Number) -> Number', summary="Performs addition of two numbers.")
def add(a, b):
    return a + b

@jsonrpc.method('Math.subtract(a=Number, b=Number) -> Number', summary="Performs subtraction of two numbers.")
def subtract(a, b):
    return a - b

@jsonrpc.method('Math.multiply(a=Number, b=Number) -> Number', summary="Performs multiplication of two numbers.")
def multiply(a, b):
    return a * b

@jsonrpc.method('Math.divide(a=Number, b=Number) -> Number', summary="Performs division of two numbers.")
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero. (JSON-RPC Error)") 
    return a / b

# --- Run App ---

if __name__ == '__main__':
    # وظیفه ۲: تنظیم برای حفظ اتصال (Protocol Version HTTP/1.1)
    WSGIRequestHandler.protocol_version = "HTTP/1.1" 
    app.run(debug=True)
