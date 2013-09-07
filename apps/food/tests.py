# -*- coding: utf-8 -*-

from audioop import reverse
from django_webtest import WebTest
from apps.common.factories import UserF


class FoodPagesTest(WebTest):
    def setUp(self):
        self.user = UserF.create()
        self.user.save()

    def test_auth_food_page(self):
        url = reverse('food_page')
        res = self.app.get(url, user=self.user)
        self.assertEquals(res.status_code, 200, 'Food page is unavalible')

    def test_unauth_food_page(self):
        url = reverse('food_page')
        res = self.app.get(url)
        self.assertEquals(res.status_code, 302, 'Food page is avalible for unauth user')

    def test_auth_eating_page(self):
        url = reverse('eating_page')
        res = self.app.get(url, user=self.user)
        self.assertEquals(res.status_code, 200, 'Eating page is unavalible')

    def test_unauth_eating_page(self):
        url = reverse('eating_page')
        res = self.app.get(url)
        self.assertEquals(res.status_code, 302, 'Eating page is avalible for unauth user')