import sys
import traceback

from tracking.models import Tracking


class ErrorTraceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):
        _, _, _traceback = sys.exc_info()
        Tracking.objects.create(
            method=request.method,
            url=request.path,
            data={
                'message': exception.args[0]
                if exception.args else 'Unknown error',
                'get': request.GET,
                'post': request.POST,
                'traceback': ''.join(traceback.format_tb(_traceback))
            }
        )
        return None
