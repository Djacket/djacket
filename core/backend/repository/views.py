from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from repository.decorators import require_existing_repo, require_existing_rev, require_access, require_owner_access
from git.object import GitTree, GitBlob, GIT_BLOB_OBJECT, GIT_TREE_OBJECT, GIT_VALID_OBJECT_KINDS
from repository.forms import RepositoryCreationForm, RepositoryArea51Form
from git.action import GIT_ACTION_ADVERTISEMENT, GIT_ACTION_RESULT
from git.decorators import git_access_required
from utils.urlparser import partition_url
from git.statistics import GitStatistics
from repository.models import Repository
from git.http import GitResponse
from git.repo import Repo


@require_http_methods(['GET'])
@require_existing_repo
@git_access_required
def get_info_refs(request, username, repository):
    """
        Responds to '/info/refs' requests for the given service, username and repository.
    """

    requested_repo = Repo(Repo.get_repository_location(username, repository))
    response = GitResponse(service=request.GET['service'], action=GIT_ACTION_ADVERTISEMENT,
                    repository=requested_repo, data=None)

    return response.get_http_info_refs()


@require_http_methods(['POST'])
@require_existing_repo
@git_access_required
@csrf_exempt
def service_rpc(request, username, repository):
    """
        Responds to 'git-receive-pack' or 'git-upload-pack' requests
            for the given username and repository.
        Decorator 'csrf_exempt' is used because git POST requests does not provide csrf cookies and
            therefore validation cannot be done.
    """

    requested_repo = Repo(Repo.get_repository_location(username, repository))
    response = GitResponse(service=request.path_info.split('/')[-1], action=GIT_ACTION_RESULT,
                    repository=requested_repo, data=request.body)

    return response.get_http_service_rpc()


@require_http_methods(['GET', 'POST'])
@login_required
def new_repository(request):
    """
        Responds to user's request to create a new repository.
    """

    if request.method == 'POST':
        form = RepositoryCreationForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('view_repository', username=request.user.username, repository=form.cleaned_data['name'])
    elif request.method == 'GET':
        form = RepositoryCreationForm()

    return render(request, 'repository/new.html', {'form': form})


@require_http_methods(['POST'])
@login_required
@require_existing_repo
@require_owner_access
def repository_area51(request, username, repository):
    """
        View for deleting a repository of user's deposit.
    """

    repository = Repository.objects.get(owner=request.user, name=repository)
    form = RepositoryArea51Form(data=request.POST, repository=repository)
    if form.is_valid():
        form.save()
        return redirect('index')
    else:
        raise Http404()


@require_http_methods(['GET'])
@require_existing_repo
@require_access
@require_existing_rev
def view_repository(request, username, repository, rev='HEAD'):
    """
        View for showing repository objects inside the given revision (either trees or blobs).
    """

    requested_repo = Repo(Repo.get_repository_location(username, repository))
    objects = _parse_repo_url(request.path_info, requested_repo, rev)
    if objects is None:
        raise Http404()
    else:
        return render(request, 'repository/repo-pjax.html',
                    {'template': 'browse', 'repo_owner': username, 'repo_name': repository,
                        'repo_lsmsg': requested_repo.get_latest_status, 'rev': rev, 'objects': objects})


@require_http_methods(['GET'])
@require_existing_repo
@require_access
@require_existing_rev
def repository_branches(request, username, repository):
    """
        View for viewing branches for repository.
    """

    requested_repo = Repo(Repo.get_repository_location(username, repository))
    branches = requested_repo.get_branches()
    return render(request, 'repository/repo-pjax.html',
                    {'template': 'branches', 'repo_owner': username, 'repo_name': repository,
                        'num_branches':len(branches), 'HEAD': requested_repo.get_head(), 'branches': branches})


@require_http_methods(['GET'])
@require_existing_repo
@require_access
@require_existing_rev
def repository_commits(request, username, repository):
    """
        View for viewing commits for repository.
    """

    requested_repo = Repo(Repo.get_repository_location(username, repository))
    commits = {branch:requested_repo.get_commits(branch) for branch in requested_repo.get_branches()}
    return render(request, 'repository/repo-pjax.html',
                    {'template': 'commits', 'repo_owner': username, 'repo_name': repository, 'commits': commits})


@require_http_methods(['GET'])
@require_existing_repo
@require_access
@require_existing_rev
def repository_graphs(request, username, repository):
    """
        View for viewing commits for repository.
    """

    requested_repo = Repo(Repo.get_repository_location(username, repository))
    branches = requested_repo.get_branches()

    return render(request, 'repository/repo-pjax.html',
                    {'template': 'graphs', 'repo_owner': username, 'repo_name': repository,
                        'repo_lsmsg': requested_repo.get_latest_status, 'num_branches': len(branches)})


@require_http_methods(['GET', 'POST'])
@require_existing_repo
@login_required
@require_owner_access
def repository_settings(request, username, repository):
    """
        View for changing/viewing repository settings.
    """

    repo = Repository.objects.get(owner=request.user, name=repository)
    if request.method == 'POST':
        form = RepositoryCreationForm(data=request.POST, user=request.user, instance=repo, edit=True)
        if form.is_valid():
            form.save()
            return redirect('view_repository', username=form.instance.owner.username, repository=form.instance.name)
    elif request.method == 'GET':
        form = RepositoryCreationForm(instance=repo, edit=True)

    return render(request, 'repository/repo-settings.html',
                    {'repo': repo, 'repo_owner': username, 'repo_name': repository, 'form': form})


def _parse_repo_url(request_path, repository, rev):
    """
        Parses url for viewing repository. Splits request url on '/' and checks parts
            to specify which revision and object should be shown.

        e.g.
            Input like "/username/repository.git/tree/master/some/folder/object.c" will return
                branch "master" and blob object "some/folder/object.c" to show.

    """

    request_sections = partition_url(request_path)
    num_sections = len(request_sections)

    if num_sections == 2:
        return repository.ls_tree(recursive=False, rev=rev)
    elif num_sections == 4 and request_sections[2] == GIT_TREE_OBJECT:
        return repository.ls_tree(recursive=False, rev=request_sections[3])
    elif num_sections > 4:
        if request_sections[2] == GIT_TREE_OBJECT:
            return GitTree(repo=repository, path='/'.join(request_sections[4:]), rev=rev).show()
        elif request_sections[2] == GIT_BLOB_OBJECT:
            return GitBlob(repo=repository, path='/'.join(request_sections[4:]), rev=rev)
    else:
        return None
