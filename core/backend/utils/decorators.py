from functools import wraps

from django.http import Http404


def require_ajax(func):
    """
        Checks to see if the request sent is of ajax type.
    """

    @wraps(func)
    def _decorator(request, *args, **kwargs):
        if request.is_ajax():
            return func(request, *args, **kwargs)
        else:
            raise Http404()
    return _decorator
