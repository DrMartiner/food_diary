# -*- coding: utf-8 -*-

from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .fields import RussianPhoneNumberField
from .fields import RussianPhoneNumberWidget
from django import forms

User = get_user_model()


class UserCreationForm(DjangoUserCreationForm):
    username = forms.EmailField(label='Телефон')

    class Meta:
        model = User

    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']).exists():
            raise ValidationError('Почта должна быть уникальной')
        return cd['email']

    def clean_username(self):
        return self.cleaned_data['username']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['username']
        if commit:
            user.save()
        return user


class UserChangeForm(DjangoUserChangeForm):
    username = forms.CharField(required=False)
    email = forms.EmailField(label='Почта')

    class Meta:
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.id = kwargs['instance'].id

    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']).exclude(id=self.id).exists():
            raise ValidationError('Почта должна быть уникальной')
        return cd['email']


class LoginForm(AuthenticationForm):
    username = RussianPhoneNumberField(label='Телефон',
                                       widget=RussianPhoneNumberWidget(attrs={'class': 'russianphonenumberwidget'}))