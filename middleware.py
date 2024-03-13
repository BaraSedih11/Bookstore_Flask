class SimpleMiddleWare(object):
    """
    Simple WSGI middleware
    """
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        print("Hello from the middleware :>")
        return self.app(environ, start_response)