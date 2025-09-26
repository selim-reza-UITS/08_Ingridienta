import logging
import time

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("myproject")

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        logger.info(f"➡️  {request.method} {request.get_full_path()} | IP: {get_client_ip(request)}")

    def process_response(self, request, response):
        duration = time.time() - getattr(request, 'start_time', time.time())
        status = response.status_code
        logger.info(f"⬅️  {status} {request.method} {request.get_full_path()} | ⏱️ {duration:.2f}s")
        return response

    def process_exception(self, request, exception):
        logger.exception(f"🔥 Exception in {request.method} {request.get_full_path()}: {exception}")

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    return x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")
