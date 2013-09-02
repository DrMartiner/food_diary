# -*- coding: utf-8 -*-

from rest_framework.serializers import HyperlinkedModelSerializer
from apps.food.models import Food
from apps.food.models import Eating
from apps.food.models import EatingFood


class FoodSerializerDisplay(HyperlinkedModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'name')


class EatingSerializerDisplay(HyperlinkedModelSerializer):
    class Meta:
        model = Eating
        fields = ('id', 'pub_date')


class EatingFoodSerializerDisplay(HyperlinkedModelSerializer):
    class Meta:
        model = EatingFood
        fields = ('id', 'eating', 'food', 'count')


class FoodSerializerSave(HyperlinkedModelSerializer):
    class Meta:
        model = Food
        exclude = ('user', )
        fields = ('name', )


class EatingSerializerSave(HyperlinkedModelSerializer):
    class Meta:
        model = Eating
        exclude = ('user', )
        fields = ('pub_date', )


class EatingFoodSerializerSave(HyperlinkedModelSerializer):
    class Meta:
        model = EatingFood
        fields = ('eating', 'food', 'count')