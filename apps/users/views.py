# -*- coding: utf-8 -*-

from django.views.generic import TemplateView


class MyProfileView(TemplateView):
    template_name = 'users/my_profile.html'