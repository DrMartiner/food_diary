# -*- coding: utf-8 -*-

from django.db.models import Q
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

    def get_list(self, request, **kwargs):
        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        objects = self.custom_sorting(objects, request)
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects, resource_uri=self.get_resource_uri(),
                                               limit=self._meta.limit, max_limit=self._meta.max_limit,
                                               collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()

        bundles = []

        for obj in to_be_serialized[self._meta.collection_name]:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle, for_list=True))

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)

    def custom_sorting(self, objects, request):
        return objects

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        kwargs.update({'user': bundle.request.user})
        super(BaseResource, self).obj_update(bundle, skip_errors=False, **kwargs)

    def obj_delete(self, bundle, **kwargs):
        super(BaseResource, self).obj_delete(bundle, user=bundle.request.user)

    class Meta:
        limit = 10
        always_return_data = True
        authorization = Authorization()
        authentication = SessionAuthentication()
        allowed_methods = ['get', 'post', 'put', 'patch', 'delete']


class FoodResource(BaseResource):
    def custom_sorting(self, objects, request):
        return objects.filter(
            Q(user=request.user) | Q(user__isnull=True)
        )

    class Meta(BaseResource.Meta):
        resource_name = 'food'
        queryset = Food.objects.all()
        filtering = {
            'id': ['exact'],
            'name': ['exact', 'contains', 'icontains', 'startwith'],
        }


class EatingResource(BaseResource):
    def custom_sorting(self, objects, request):
        return objects.filter(user=request.user)

    class Meta(BaseResource.Meta):
        resource_name = 'eating'
        queryset = Eating.objects.all()
        filtering = {
            'id': ['exact'],
            'pub_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
        }


class EatingFoodResource(BaseResource):
    def custom_sorting(self, objects, request):
        return objects.filter(user=request.user)

    class Meta(BaseResource.Meta):
        resource_name = 'eatingfood'
        queryset = EatingFood.objects.all()
        filtering = {
            'eating__id': ['exact'],
            'eating__pub_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
        }