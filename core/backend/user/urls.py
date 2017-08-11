from django.conf.urls import url
from django.contrib.auth.views import logout

from user.views import user_login, user_register, user_settings, user_profile, user_area51

urlpatterns = [
    url(r'register$', user_register, name='user_register'),
    url(r'login$', user_login, name='user_login'),
    url(r'logout$', logout, {'next_page': 'index'}, name='user_logout'),
    url(r'settings/profile$', user_profile, name='user_profile'),
    url(r'settings/area51$', user_area51, name='user_area51'),
    url(r'settings$', user_settings, name='user_settings'),
]
