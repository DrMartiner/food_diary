# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from tastypie.api import Api
from .resources_v1 import FoodResource
from .resources_v1 import EatingResource
from .resources_v1 import EatingFoodResource

v1_api = Api()
v1_api.register(FoodResource())
v1_api.register(EatingResource())
v1_api.register(EatingFoodResource())

urlpatterns = patterns('',
    url(r'^', include(v1_api.urls)),
)