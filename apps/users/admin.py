# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .forms import UserChangeForm
from .forms import UserCreationForm

User = get_user_model()


class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

admin.site.register(User, UserAdmin)