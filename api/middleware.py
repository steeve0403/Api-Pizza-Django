from django.utils.deprecation import MiddlewareMixin
from api_pizza_django import settings
import logging

logger = logging.getLogger(__name__)

class LogRequestsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if settings.DEBUG:
            logger.info(f"Request {request.method} to {request.path}")

    def process_exception(self, request, exception):
        if settings.DEBUG:
            logger.info(f"Exception at the {request.method} to {request.path}: {exception}")
