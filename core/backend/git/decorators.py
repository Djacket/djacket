from functools import wraps

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden

from git.service import GIT_SERVICE_RECEIVE_PACK, GIT_SERVICE_UPLOAD_PACK
from repository.models import Repository, RepositoryAccess
from user.auth import base_auth


def git_access_required(func):
    """
        Checks to see if a repository is accessible to user. There are 3 scenarios:
            1) If repository is private and user is doing a 'git-clone' or 'git-pull': In this
                    case only users who have access to repository are admitted.
            2) If repository is public and user is doing a 'git-clone' or 'git-pull': This operation
                    is ok since repository is available for everyone.
            3) If user is committing something to repository then regardless of being a public/private
                    repository, user should be authenticated and has access to repository.
    """

    @wraps(func)
    def _decorator(request, *args, **kwargs):
        service = _parse_git_service(request.build_absolute_uri())
        user = User.objects.get(username=kwargs['username'])
        repo = Repository.objects.get(owner=user, name=kwargs['repository'])
        if service == GIT_SERVICE_UPLOAD_PACK and repo.private: # private repo and doing a 'git-clone' or 'git-pull'
            return _check_access(request, func, *args, **kwargs)
        elif service == GIT_SERVICE_UPLOAD_PACK and not repo.private: # public repo and doing a 'git-clone' or 'git-pull'
            return func(request, *args, **kwargs)
        elif service == GIT_SERVICE_RECEIVE_PACK: # doing a 'git-commit'
            return _check_access(request, func, *args, **kwargs)
    return _decorator


def _check_access(request, func, *args, **kwargs):
    """
        Checks user's authentication and access to repository.
    """

    if request.META.get('HTTP_AUTHORIZATION'):
        user = base_auth(request.META['HTTP_AUTHORIZATION'])
        if user:
            repo = Repository.objects.get(owner=user, name=kwargs['repository'])
            access = RepositoryAccess.objects.get(user=user, repository=repo)
            if access:
                return func(request, *args, **kwargs)
            else:   # User has no access to repository.
                return HttpResponseForbidden('Access forbidden.')
        else:   # User is not registered on Djacket.
            return HttpResponseForbidden('Access forbidden.')
    res = HttpResponse()
    res.status_code = 401   # Basic authentication is needed.
    res['WWW-Authenticate'] = 'Basic'
    return res


def _parse_git_service(request_path):
    """
        Parses request url and specifies which git service is requested.
    """

    if request_path.endswith('git-upload-pack'):
        return GIT_SERVICE_UPLOAD_PACK
    elif request_path.endswith('git-receive-pack'):
        return GIT_SERVICE_RECEIVE_PACK
    else:
        return None
