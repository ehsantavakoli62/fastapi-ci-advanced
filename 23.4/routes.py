# routes.py

import json
from typing import Dict, Any, Callable, List, Tuple

# تعریف نوع برای مسیرها
RouteHandler = Callable[[Dict[str, str]], str]

class SimpleWSGIApp:
    """
    پیاده‌سازی یک WSGI Application ساده با پشتیبانی از دکوراتور مسیرها.
    """
    def __init__(self):
        # ساختار نگهداری مسیرها: {"/hello": say_hello, "/hello/<name>": say_hello_with_name}
        self.routes: Dict[str, RouteHandler] = {}

    def route(self, uri: str) -> Callable[[RouteHandler], RouteHandler]:
        """
        دکوراتور برای تعریف مسیرهای URL.
        """
        def decorator(handler: RouteHandler) -> RouteHandler:
            self.routes[uri] = handler
            return handler
        return decorator

    def __call__(self, environ: Dict[str, Any], start_response: Callable):
        """
        متد اصلی WSGI Application
        """
        request_uri = environ.get('REQUEST_URI', '/')
        status = '200 OK'
        headers: List[Tuple[str, str]] = [('Content-type', 'application/json')]
        response_body = json.dumps({"error": "404 Not Found", "uri": request_uri}, indent=4)
        
        # 1. جستجو در مسیرهای دقیق (بدون پارامتر)
        if request_uri in self.routes:
            handler = self.routes[request_uri]
            response_body = handler({})
            
        # 2. جستجو در مسیرهای پارامتریک (مانند /hello/user)
        else:
            found = False
            uri_parts = [p for p in request_uri.split('/') if p]
            
            for route, handler in self.routes.items():
                route_parts = [p for p in route.split('/') if p]
                
                # بررسی تعداد بخش‌ها و یافتن پارامترها
                if len(uri_parts) == len(route_parts):
                    path_params: Dict[str, str] = {}
                    match = True
                    for i in range(len(uri_parts)):
                        route_part = route_parts[i]
                        uri_part = uri_parts[i]
                        
                        if route_part.startswith('<') and route_part.endswith('>'):
                            # این یک پارامتر است
                            param_name = route_part[1:-1]
                            path_params[param_name] = uri_part
                        elif route_part != uri_part:
                            # بخش‌های غیرپارامتری مطابقت ندارند
                            match = False
                            break
                    
                    if match:
                        response_body = handler(path_params)
                        status = '200 OK'
                        found = True
                        break

            if found == False:
                 status = '404 Not Found'
                 
        start_response(status, headers)
        return [response_body.encode('utf-8')]

# ایجاد نمونه برنامه
app = SimpleWSGIApp()

# --- تعریف Endpoints (مشابه Flask) ---

@app.route("/hello")
def say_hello(params: Dict[str, str]):
    """Default behavior for /hello"""
    return json.dumps({"response": "Hello, world!"}, indent=4)

@app.route("/hello/<name>")
def say_hello_with_name(params: Dict[str, str]):
    """Personalized behavior for /hello/user"""
    name = params.get('name', 'guest')
    return json.dumps({"response": f"Hello, {name}!"}, indent=4)

if __name__ == '__main__':
    # این کد برای اجرای مستقیم و تست است
    from wsgiref.simple_server import make_server
    with make_server('', 8000, app) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()
