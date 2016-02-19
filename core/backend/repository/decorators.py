from functools import wraps

from django.http import Http404
from django.contrib.auth.models import User

from repository.models import Repository
from git.repo import Repo


def require_existing_repo(func):
    """
        Checks to see if requested repository is available on user's deposit.
            Raises 404 if not.
    """

    @wraps(func)
    def _decorator(request, *args, **kwargs):
        try:
            user = User.objects.get(username=kwargs['username'])
            repo = Repository.objects.get(owner=user, name=kwargs['repository'])
            return func(request, *args, **kwargs)
        except:
            raise Http404()
    return _decorator


def require_existing_rev(func):
    """
        Checks to see if requested revision exists in repository.
            Raises 404 if not.
    """

    @wraps(func)
    def _decorator(request, *args, **kwargs):
        try:
            repo = Repo(Repo.get_repository_location(kwargs['username'], kwargs['repository']))
            branches = repo.get_branches()
            if 'rev' not in kwargs or kwargs['rev'] in branches + ['HEAD']:
                return func(request, *args, **kwargs)
            else:
                raise Http404()
        except:
            raise Http404()
    return _decorator


def require_access(func):
    """
        Checks to see if requesting user has access to repository. If repository
            is private then only it's owner has access to it. If not, then everyone
            can see or clone this repository.
        Raises 404 if not.
    """

    @wraps(func)
    def _decorator(request, *args, **kwargs):
        try:
            user = User.objects.get(username=kwargs['username'])
            repo = Repository.objects.get(owner=user, name=kwargs['repository'])
            if repo.private and request.user.id != user.id:
                raise Http404()
            else:
                return func(request, *args, **kwargs)
        except:
            raise Http404()
    return _decorator


def require_owner_access(func):
    """
        Only allows actions on repository if requesting user is repository owner.
            For example for getting access to repository settings.
        Raises 404 if not.
    """

    @wraps(func)
    def _decorator(request, *args, **kwargs):
        if request.user.username != kwargs['username']:
            raise Http404()
        else:
            return func(request, *args, **kwargs)
    return _decorator


def require_valid_readme(func):
    """
        Checks to see if requested README is a valid text README file.
            Raises 404 if not.
    """

    @wraps(func)
    def _decorator(request, *args, **kwargs):
        if request.path_info.endswith('README.md') or request.path_info.endswith('README.rst'):
            return func(request, *args, **kwargs)
        else:
            raise Http404()
    return _decorator
