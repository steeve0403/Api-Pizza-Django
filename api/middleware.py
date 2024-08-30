from django.utils.deprecation import MiddlewareMixin

class LogRequestsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(f"Requête {request.method} à {request.path}")