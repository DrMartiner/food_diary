# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class HomePage(TemplateView):
    template_name = 'simple_page/home_page.html'


class MyDiaryPage(TemplateView):
    template_name = 'simple_page/my_diary.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MyDiaryPage, self).dispatch(request, *args, **kwargs)