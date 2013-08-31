# -*- coding: utf-8 -*-

from django.db.models import Q
from django.http import Http404
from django.views.generic import View
from django.forms import model_to_dict
from rest_framework import status
from apps.common.http import JSONResponse
from rest_framework.response import Response
from .serializers import FoodSerializerSave
from .serializers import EatingSerializerSave
from .serializers import EatingFoodSerializerSave
from .serializers import FoodSerializerDisplay
from .serializers import EatingSerializerDisplay
from .serializers import EatingFoodSerializerDisplay
from .models import Food
from .models import Eating
from .models import EatingFood


class FoodListAPI(View):
    def get(self, request, format=None):
        startwith = request.GET.get('startwith')
        if not startwith:
            raise Http404
        if len(startwith) < 2:
            return JSONResponse([])

        qset = Food.objects.filter(
            Q(user__isnull=True) & Q(user=request.user) & Q(name__startwith=startwith)
        )
        serialize = FoodSerializerDisplay(qset, many=True)
        return JSONResponse(serialize)

    def post(self, request, format=None):
        serializer = FoodSerializerSave(data=request.DATA)
        if serializer.is_valid():
            obj = serializer.save(commit=False)
            obj.user = request.user
            obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EatingListAPI(View):
    def get(self, request, format=None):
        qset = Eating.objects.filter(user=request.user)
        serialize = EatingSerializerDisplay(qset, many=True)
        return JSONResponse(serialize)

    def post(self, request, format=None):
        serializer = FoodSerializerSave(data=request.DATA)
        if serializer.is_valid():
            obj = serializer.save(commit=False)
            obj.user = request.user
            obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EatingFoodListAPI(View):
    def get(self, request, format=None):
        eating = request.GET.get('eating')
        if not eating:
            raise Http404

        qset = EatingFood.objects.filter(user=request.user, eating=eating)
        serialize = EatingFoodSerializerDisplay(qset, many=True)
        return JSONResponse(serialize)

    def post(self, request, format=None):
        serializer = FoodSerializerSave(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)