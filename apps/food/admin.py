# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Food
from .models import Eating
from .models import EatingFood


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', )


class EatingFoodInline(admin.TabularInline):
    extra = 0
    model = EatingFood


class EatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'pub_date')
    list_filter = ('pub_date', )
    inlines = (EatingFoodInline, )


admin.site.register(Food, FoodAdmin)
admin.site.register(Eating, EatingAdmin)