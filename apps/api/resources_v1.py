# -*- coding: utf-8 -*-
import json
from annoying.functions import get_object_or_None

from django.db.models import Q
from django.forms import model_to_dict
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication
from apps.food.models import Food
from apps.food.models import Eating
from apps.food.models import EatingFood


class BaseResource(ModelResource):
    def determine_format(self, request):
        return 'application/json'

    def obj_create(self, bundle, **kwargs):
        return super(BaseResource, self).obj_create(bundle, user=bundle.request.user)

    def obj_create(self, bundle, **kwargs):
        kwargs.update({'user': bundle.request.user})
        return super(BaseResource, self).obj_create(bundle, **kwargs)

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        kwargs.update({'user': bundle.request.user})
        return super(BaseResource, self).obj_update(bundle, skip_errors=skip_errors, **kwargs)

    def obj_delete(self, bundle, **kwargs):
        kwargs.update({'user': bundle.request.user})
        return super(BaseResource, self).obj_delete(bundle, **kwargs)

    class Meta:
        limit = 10
        always_return_data = True
        authorization = Authorization()
        authentication = SessionAuthentication()
        allowed_methods = ['get', 'post', 'put', 'patch', 'delete']


class FoodResource(BaseResource):
    def apply_filters(self, request, applicable_filters):
        qset = super(FoodResource, self).apply_filters(request, applicable_filters)
        return qset.filter(
            Q(user=request.user) | Q(user__isnull=True)
        )

    def obj_create(self, bundle, **kwargs):
        food = get_object_or_None(Food,
                                  name=bundle.data['name'],
                                  user=bundle.request.user,)
        if food:
            bundle.data.update({'id': food.pk})
            bundle.obj = self._meta.object_class()
            for key, value in kwargs.items():
                setattr(bundle.obj, key, value)
            return self.full_hydrate(bundle)

        kwargs.update({'user': bundle.request.user})
        return super(ModelResource, self).obj_create(bundle, **kwargs)

    class Meta(BaseResource.Meta):
        resource_name = 'food'
        queryset = Food.objects.all()
        filtering = {
            'id': ['exact'],
            'name': ['exact', 'contains', 'icontains', 'startwith'],
        }


class EatingResource(BaseResource):
    def apply_filters(self, request, applicable_filters):
        qset = super(EatingResource, self).apply_filters(request, applicable_filters)
        return qset.filter(user=request.user)

    def alter_detail_data_to_serialize(self, request, data):
        data.data['eatingfoods'] = data.obj.eatingfoods
        return data

    def alter_list_data_to_serialize(self, request, data):
        results = []
        for bundle in data['objects']:
            bundle.data['eatingfoods'] = bundle.obj.eatingfoods
            results.append(bundle)
        return data

    class Meta(BaseResource.Meta):
        resource_name = 'eating'
        queryset = Eating.objects.all()
        allowed_methods = ['get', 'post', 'delete']
        filtering = {
            'id': ['exact'],
            'pub_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
        }


class EatingFoodResource(BaseResource):
    def apply_filters(self, request, applicable_filters):
        qset = super(EatingFoodResource, self).apply_filters(request, applicable_filters)
        return qset.filter(user=request.user)

    def obj_create(self, bundle, **kwargs):
        kwargs.update({
            'food_id': bundle.data.get('food_id'),
            'eating_id': bundle.data.get('eating_id'),
            'eating_user': bundle.request.user,
        })
        return super(BaseResource, self).obj_create(bundle, **kwargs)

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        kwargs.update({'eating__user': bundle.request.user})
        super(ModelResource, self).obj_update(bundle, skip_errors=skip_errors, **kwargs)

    def obj_delete(self, bundle, **kwargs):
        kwargs.update({'eating__user': bundle.request.user})
        super(ModelResource, self).obj_delete(bundle, **kwargs)

    class Meta(BaseResource.Meta):
        resource_name = 'eatingfood'
        queryset = EatingFood.objects.all()
        filtering = {
            'eating__id': ['exact'],
            'eating__pub_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
        }