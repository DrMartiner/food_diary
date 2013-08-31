# -*- coding: utf-8 -*-

from django_webtest import WebTest
from django.core.urlresolvers import reverse


class SimplePageTest(WebTest):
    def test_home_page(self):
        url = reverse('home_page')
        res = self.app.get(url)
        self.assertEquals(res.status_code, 200, 'Home page is unavalible')
