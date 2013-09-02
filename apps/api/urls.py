# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import FoodList
from .views import FoodDetail

urlpatterns = patterns('',
                       url(r'^food/$', FoodList.as_view()),
                       url(r'^food/(?P<pk>[0-9]+)/$', FoodDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)