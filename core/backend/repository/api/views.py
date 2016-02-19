import json

from django.http import Http404, HttpResponse
from django.views.decorators.http import require_http_methods

from repository.decorators import require_existing_repo, require_existing_rev, require_access, require_valid_readme
from git.statistics import DataPresentation
from utils.urlparser import partition_url
from utils.decorators import require_ajax
from git.statistics import GitStatistics
from git.object import GitBlob
from git.repo import Repo

weekly, monthly = GitStatistics.WEEKLY_INTERVALS, GitStatistics.MONTHLY_INTERVALS
py, js = DataPresentation.PY_FORMAT, DataPresentation.JS_FORMAT


@require_http_methods(['GET'])
@require_access
@require_existing_repo
@require_ajax
def commits_stats(request, username, repository):
    """
        Returns number of commits for the given repository.
    """

    repo = Repo(Repo.get_repository_location(username, repository))
    stats = GitStatistics(repo, repo.get_head())

    return HttpResponse(json.dumps({'weekly': stats.for_commits(weekly, js), 'monthly': stats.for_commits(monthly, js)}))


@require_http_methods(['GET'])
@require_access
@require_existing_repo
@require_existing_rev
@require_valid_readme
@require_ajax
def readme(request, username, repository, rev):
    """
        Returns README content of a folder inside the given repository.
    """

    repo = Repo(Repo.get_repository_location(username, repository))
    request_sections = partition_url(request.path_info)
    rdm = GitBlob(repo=repo, path='/'.join(request_sections[5:]), rev=rev).show()

    return HttpResponse(rdm)
