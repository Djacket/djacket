from django.shortcuts import render
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User, AnonymousUser
from django.views.decorators.http import require_http_methods

from user.forms import UserRegistrationForm
from user.views import user_deposit


@require_http_methods(['GET'])
def index(request):
    """
        View for index page. If request user is not authenticated then Djacket intro
            page is shown, else if user is authenticated his/her deposit is shown.
    """

    if request.user.is_authenticated():
        return user_deposit(request, request.user.username)
    else:
        return render(request, 'index.html', {'active': 'login', REDIRECT_FIELD_NAME: request.GET.get(REDIRECT_FIELD_NAME, '')})
