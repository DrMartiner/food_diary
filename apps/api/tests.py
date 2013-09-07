# -*- coding: utf-8 -*-

import json
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from annoying.functions import get_object_or_None
from apps.common.factories import UserF
from apps.common.factories import FoodF
from apps.food.models import Food


class FoodTest(WebTest):
    csrf_checks = False

    def setUp(self):
        self.user = UserF.create()
        self.user.save()
        self.content_type = 'application/json'

    def test_create(self):
        url = reverse('api_dispatch_list', kwargs={'api_name': 'v1', 'resource_name': 'food'})
        params = json.dumps({'name': 'My faster food'})
        self.app.post(url, params=params, user=self.user, content_type=self.content_type)
        food = get_object_or_None(Food, name='My faster food', user=self.user)
        self.assertIsNotNone(food, 'Food was not created')
        food.delete()

    def test_list(self):
        food = FoodF.create(user=self.user)
        food.save()
        food = FoodF.create(user=None)
        food.save()
        user = UserF()
        user.save()
        food = FoodF.create(user=user)
        food.save()

        url = reverse('api_dispatch_list', kwargs={'api_name': 'v1', 'resource_name': 'food'})
        req = self.app.get(url, user=self.user)

        foods = json.loads(req.content)
        self.assertEquals(foods['meta']['total_count'], 2, '')

    def test_update_self_food(self):
        food = FoodF.create(user=self.user)
        food.save()

        url = reverse('api_dispatch_detail', kwargs={
            'api_name': 'v1',
            'resource_name': 'food',
            'pk': food.pk,
        })

        params = {'name': u'New food name'}
        self.app.put(url, params=json.dumps(params), user=self.user, content_type=self.content_type)

        food = get_object_or_None(Food, pk=food.pk)
        self.assertEquals(food.name, params['name'], 'Food was not changed')

    def test_update_piblic_food(self):
        food = FoodF.create(user=None)
        food.save()

        url = reverse('api_dispatch_detail', kwargs={
            'api_name': 'v1',
            'resource_name': 'food',
            'pk': food.pk,
        })

        params = {'name': u'New food name'}
        self.app.put(url, params=json.dumps(params), user=self.user, content_type=self.content_type)

        food = get_object_or_None(Food, pk=food.pk)
        self.assertNotEquals(food.name, params['name'], 'Public food was changed')

    def test_update_alian_food(self):
        user = UserF.create()
        user.save()
        food = FoodF.create(user=user)
        food.save()

        url = reverse('api_dispatch_detail', kwargs={
            'api_name': 'v1',
            'resource_name': 'food',
            'pk': food.pk,
        })

        params = {'name': u'New food name'}
        self.app.put(url, params=json.dumps(params), user=self.user, content_type=self.content_type)

        food = get_object_or_None(Food, pk=food.pk)
        self.assertNotEquals(food.name, params['name'], 'Alian food was changed')

    def test_del_self_food(self):
        food = FoodF.create(user=self.user)
        food.save()

        url = reverse('api_dispatch_detail', kwargs={
            'api_name': 'v1',
            'resource_name': 'food',
            'pk': food.pk,
        })
        self.app.delete(url, user=self.user)

        food = get_object_or_None(Food, pk=food.pk)
        self.assertIsNone(food, 'Food was not delete')

    def test_del_public_food(self):
        food = FoodF.create(user=None)
        food.save()

        url = reverse('api_dispatch_detail', kwargs={
            'api_name': 'v1',
            'resource_name': 'food',
            'pk': food.pk,
        })
        self.app.delete(url, user=self.user, expect_errors=True)

        food = get_object_or_None(Food, pk=food.pk)
        self.assertIsNotNone(food, 'Public food was delete')

    def test_del_alian_food(self):
        user = UserF()
        user.save()
        food = FoodF.create(user=user)
        food.save()

        url = reverse('api_dispatch_detail', kwargs={
            'api_name': 'v1',
            'resource_name': 'food',
            'pk': food.pk,
        })
        self.app.delete(url, user=self.user, expect_errors=True)

        food = get_object_or_None(Food, pk=food.pk)
        self.assertIsNotNone(food, 'Alian food was delete')