from django.conf.urls import include, url

from repository.views import get_info_refs, service_rpc, new_repository, \
                                view_repository, repository_settings, repository_area51,    \
                                repository_branches, repository_commits, repository_graphs


urlpatterns = [
    url(r'new$', new_repository, name='new_repository'),
    url(r'^api/', include('repository.api.urls')),
    url(r'(?P<username>\w+)/(?P<repository>[-\w]+).git/info/refs', get_info_refs, name='get_info_refs'),
    url(r'(?P<username>\w+)/(?P<repository>[-\w]+).git/git-upload-pack$', service_rpc, name='service_rpc'),
    url(r'(?P<username>\w+)/(?P<repository>[-\w]+).git/git-receive-pack$', service_rpc, name='service_rpc'),
    url(r'(?P<username>\w+)/(?P<repository>[-\w]+).git/settings$', repository_settings, name='repository_settings'),
    url(r'(?P<username>\w+)/(?P<repository>[-\w]+).git/area51$', repository_area51, name='repository_area51'),
    url(r'(?P<username>\w+)/(?P<repository>[-\w]+).git/branches$', repository_branches, name='repository_branches'),
    url(r'(?P<username>\w+)/(?P<repository>[-\w]+).git/commits$', repository_commits, name='repository_commits'),
    url(r'(?P<username>\w+)/(?P<repository>[-\w]+).git/graphs$', repository_graphs, name='repository_graphs'),
    url(r'(?P<username>\w+)/(?P<repository>[-\w]+).git/tree/(?P<rev>[-\w]+)/*', view_repository, name='view_repository'),
    url(r'(?P<username>\w+)/(?P<repository>[-\w]+).git/blob/(?P<rev>[-\w]+)/*', view_repository, name='view_repository'),
    url(r'(?P<username>\w+)/(?P<repository>[-\w]+).git$', view_repository, name='view_repository'),
]
