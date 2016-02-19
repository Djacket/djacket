from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url

from user.views import user_deposit
from djacket.views import index


# Djacket main urls will be addressed here.

urlpatterns = [
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), # serve static medias on /media/*
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')), # project docs view.
    url(r'^admin/', include(admin.site.urls)), # admin interface.
    url(r'^', include('repository.urls')),  # import repository app urls with no prefix.
    url(r'^account/', include('user.urls')),  # import user app urls with 'account' prefix.
    url(r'^(?P<username>\w+)$', user_deposit, name='user_deposit'),  # show user deposit for url '/username'.
    url(r'^$', index, name='index'),  # index changes to logged in user if he/she is authenticated or to djacket intro if not.
]

# serve static medias on /media/* while DEBUG settings are on
if settings.DEBUG:
    urlpatterns = urlpatterns + \
        [url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),]
