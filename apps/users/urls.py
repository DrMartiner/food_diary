# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from registration.views import register
from .views import MyProfileView
from .forms import RegistrationForm
from .forms import LoginForm

urlpatterns = patterns('',
    url(r'^register/$', register,
       {'backend': 'apps.users.backend.RegisterBackend', 'form_class': RegistrationForm},
       name='registration_register'),
    url(r'^my-profile/$', MyProfileView.as_view(), name='users_myprofile'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'authentication_form': LoginForm}, name='login'),
    url(r'^', include('registration.backends.default.urls')),
    url(r'^', include('django.contrib.auth.urls')),
)