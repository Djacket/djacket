from django.conf.urls import url

from repository.api.views import commits_stats, readme


urlpatterns = [
    url(r'(?P<username>\w+)/(?P<repository>[-\w]+).git/commits_stats$', commits_stats, name='commits_stats'),
    url(r'(?P<username>\w+)/(?P<repository>[-\w]+).git/readme/(?P<rev>[-\w]+)/*', readme, name='readme'),
]
