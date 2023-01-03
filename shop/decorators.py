from functools import wraps

from django.http import HttpResponseForbidden


def ajax_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            return HttpResponseForbidden('Forbidden')
        return view_func(request, *args, *kwargs)
    return _wrapped_view
