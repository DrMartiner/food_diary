# -*- coding: utf-8 -*-

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from annoying.functions import get_object_or_None
from django.contrib.auth.forms import AuthenticationForm
from .fields import RussianPhoneNumberField
from django import forms

User = get_user_model()


class UserCreationForm(DjangoUserCreationForm):
    username = forms.EmailField(label='Телефон')

    class Meta:
        model = User

    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email__iexact=cd['email']).exists():
            raise ValidationError('Пользователь с такой почтой уже зарегистрирован')
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
    username = RussianPhoneNumberField(label='Телефон')

    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(request, *args, **kwargs)

        self.error_messages['invalid_login'] =\
            u"Пожалуйста, введите корректный номер телефона и пароль. Пароль чувствителен к регистру"

        self.helper = FormHelper()
        self.helper.form_action = 'login'
        self.helper.form_class = 'well'
        self.helper.layout = Layout(
            'username',
            'password',
            FormActions(
                Submit('submit', u'Войти')
            )
        )


class RegistrationForm(forms.ModelForm):
    phone = RussianPhoneNumberField(label='Мобильный телефон', required=True,
                                    help_text='Телефон будет использоваться в качестве логина.')
    contract = forms.BooleanField(widget=forms.CheckboxInput(),
                                  label=u'Согласен с условиями <a target="_blank" href="/contract/">договора</a>')

    def clean_phone(self):
        user = get_object_or_None(User, username=self.cleaned_data['phone'])
        if user:
            raise forms.ValidationError(u'Пользователь с таким телефоном уже зарегистрирован в системе.')
        return self.cleaned_data['phone']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True
        self.fields['email'].label = u'Электро почта'
        self.fields['first_name'].required = True
        self.fields['contract'].required = True


        self.helper = FormHelper()
        self.helper.form_action = 'registration_register'
        self.helper.form_class = 'well'
        self.helper.layout = Layout(
            'phone',
            'email',
            'first_name',
            'last_name',
            'sex',
            'birth_date',
            'contract',
            FormActions(
                Submit('submit', u'Зарегистрироваться')
            )
        )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'sex', 'birth_date', 'email')
        widgets = {
            'sex': forms.RadioSelect(),
        }