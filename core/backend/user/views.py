from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login as auth_login
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.http import is_safe_url
from django.conf import settings
from django.http import Http404

from repository.models import Repository
from user.decorators import redirect_if_authorized
from user.forms import UserRegistrationForm, UserInfoForm, UserProfileForm, UserArea51Form


@require_http_methods(['POST'])
@redirect_if_authorized
def user_login(request):
    """
        View for logging users in.
    """

    redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME, ''))
    login_form = AuthenticationForm(request, data=request.POST)
    if login_form.is_valid():
        # Ensure the user-originating redirection url is safe.
        if not is_safe_url(url=REDIRECT_FIELD_NAME, host=request.get_host()):
            redirect_to = settings.LOGIN_REDIRECT_URL
        # Okay, security check complete. Log the user in.
        auth_login(request, login_form.get_user())
        return redirect(settings.LOGIN_REDIRECT_URL if redirect_to == '' else redirect_to)
    else:
        return render(request, 'index.html', {'login_form': login_form, 'display': 'block', 'active': 'login'})


@require_http_methods(['POST'])
@redirect_if_authorized
def user_register(request):
    """
        View for registering new users. If user is already authenticated view redirects
            to index page.
    """

    register_form = UserRegistrationForm(request.POST)
    if register_form.is_valid():
        register_form.save()
        registered_user = authenticate(username=register_form.cleaned_data['username'],
                                    password=register_form.cleaned_data['password'])
        auth_login(request, registered_user)
        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'index.html', {'register_form': register_form, 'display': 'block', 'active': 'register'})


@require_http_methods(['GET'])
def user_deposit(request, username):
    """
        View for viewing user's deposit (git repositories).
    """

    try:
        target_user = User.objects.get(username=username)
        if target_user == request.user:
            repos = Repository.objects.all_repositores(user=target_user)
        else:
            repos = Repository.objects.public_repositores(user=target_user)
    except:
        raise Http404()

    return render(request, 'user/deposit.html', {'repos': repos, 'target_user': target_user})


@login_required
@require_http_methods(['GET', 'POST'])
def user_settings(request):
    """
        View for viewing/changing user's info settings.
    """

    if request.method == 'POST':
        info_form, profile_form = UserInfoForm(request.POST, instance=request.user), UserProfileForm(user=request.user)
        if info_form.is_valid():
            info_form.save()
    elif request.method == 'GET':
        info_form, profile_form = UserInfoForm(instance=request.user), UserProfileForm(user=request.user)

    return render(request, 'user/user-settings.html',
                        {'active': 'info', 'info_form': info_form, 'profile_form': profile_form})


@login_required
@require_http_methods(['POST'])
def user_profile(request):
    """
        View for changing user's profile settings.
    """

    info_form = UserInfoForm(instance=request.user)
    profile_form = UserProfileForm(request.POST, request.FILES, user=request.user)

    if profile_form.is_valid():
        profile_form.save()

    return render(request, 'user/user-settings.html',
                        {'active': 'profile', 'info_form': info_form, 'profile_form': profile_form})


@login_required
@require_http_methods(['POST'])
def user_area51(request):
    """
        View for deleting a user account entirely.
    """

    form = UserArea51Form(request.POST, user=request.user)
    if form.is_valid():
        form.save()
        return redirect('index')
    else:
        raise Http404()
