# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from .forms import LoginForm

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'authentication_form': LoginForm}, name='login'),
    url(r'^', include('django.contrib.auth.urls')),
)