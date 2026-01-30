"""
WSGI Middleware for request performance tracking.
"""
import time
import logging

logger = logging.getLogger(__name__)

class RequestPerformanceMiddleware:
    """
    Middleware to calculate and add request processing time to headers.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        start_time = time.time()
        
        def custom_start_response(status, headers, exc_info=None):
            duration = time.time() - start_time
            # Add timing header
            headers.append(('X-Processing-Time', str(round(duration, 4))))
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)
