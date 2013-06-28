from django.conf.urls import patterns, include, url
from email_registration.views import EmailRegistrationView

urlpatterns = patterns('',
    #customize user registration form
    url(r'^register/$', EmailRegistrationView.as_view()),
    (r'^accounts/', include('registration.backends.default.urls')),
)
