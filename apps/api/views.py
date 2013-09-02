# -*- coding: utf-8 -*-

from django.db.models import Q
from django.http import Http404
from django.views.generic import View
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.views import APIView
from apps.common.http import JSONResponse
from rest_framework.response import Response
from .serializers import FoodSerializerSave
from .serializers import EatingSerializerSave
from .serializers import EatingFoodSerializerSave
from .serializers import FoodSerializerDisplay
from .serializers import EatingSerializerDisplay
from .serializers import EatingFoodSerializerDisplay
from apps.food.models import Food
from apps.food.models import Eating
from apps.food.models import EatingFood


class FoodList(APIView):
    def get(self, request, format=None):
        foods = Food.objects.filter(
            Q(user__isnull=True) | Q(user=request.user)
        )
        serializer = FoodSerializerDisplay(foods, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FoodSerializerSave(data=request.DATA)
        if serializer.is_valid():
            food = serializer.save()
            food.user = request.user
            food.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodDetail(APIView):
    def get_object(self, pk):
        try:
            return Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        food = self.get_object(pk)
        if food.user == request.user or food.user is None:
            serializer = FoodSerializerDisplay(food)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk, format=None):
        food = self.get_object(pk)
        serializer = Food(food, data=request.DATA)
        if serializer.is_valid():
            food = serializer.save()
            food.user = request.user
            food.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        food = self.get_object(pk)
        if food.user == request.user:
            food.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)