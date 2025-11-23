# app.py (بخش‌های تغییر یافته)
# ... (کد قبلی)

from flasgger import Swagger, swag_from
from werkzeug.serving import WSGIRequestHandler # برای وظیفه ۲

# ... (API initialization)
app = Flask(__name__)

# حذف api = Api(...) (اگر از Flask-RESTX استفاده می‌کردید)
# و جایگزینی با Swagger
Swagger(app) # تنظیمات Flasgger

# ... (کلاس BookListResource)
@book_ns.route('/')
class BookListResource(Resource):
    """Handles book creation"""
    
    # استفاده از مستندسازی YAML
    @swag_from('./docs/book_post.yml') 
    def post(self):
        # ... (کد قبلی)
        pass

# ... (کلاس AuthorListResource)
@author_ns.route('/')
class AuthorListResource(Resource):
    """Handles author creation"""
    
    # استفاده از مستندسازی JSON/Dict
    @swag_from('./docs/author_post.json')
    def post(self):
        # ... (کد قبلی)
        pass
        
if __name__ == '__main__':
    # تنظیم برای حفظ اتصال در تست سرعت (وظیفه ۲)
    WSGIRequestHandler.protocol_version = "HTTP/1.1" 
    app.run(debug=True)
