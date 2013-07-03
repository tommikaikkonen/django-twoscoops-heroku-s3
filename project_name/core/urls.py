from django.conf.urls import patterns, include, url
from core.views import UserDetailView, UserUpdateView

urlpatterns = patterns('',
    (r'^login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'registration/login.html',}
    ),
    (r'^logout/$', 'django.contrib.auth.views.logout', 
        {'next_page': '/login/',}
    ),
    url(r'^user/(?P<pk>[-_\w]+)/$', UserDetailView.as_view(), name='user-detail'
    ),
    url(r'^user/(?P<pk>[-_\w]+)/edit/$', UserUpdateView.as_view(), name='user-update'
    ),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)
