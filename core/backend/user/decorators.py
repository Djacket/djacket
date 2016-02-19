from functools import wraps

from django.shortcuts import redirect
from django.conf import settings


def redirect_if_authorized(func):
    """
        Redirects user to the given view (identified by 'view_name' parameter)
            if user is authenticated.
    """

    @wraps(func)
    def _decorator(request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return func(request, *args, **kwargs)
    return _decorator
