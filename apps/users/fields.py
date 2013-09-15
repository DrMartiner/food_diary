# -*- coding: utf-8 -*-

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe


class RussianPhoneNumberWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        wigs = (forms.TextInput(attrs={'maxlength': '3', 'class': 'phone_number__code'}),
                forms.TextInput(attrs={'maxlength': '7', 'class': 'phone_number__number'}))
        super(RussianPhoneNumberWidget, self).__init__(wigs, attrs)

    def decompress(self, value):
        if value:
            return [value[2:5], value[5:]]
        return [None, None]

    def render(self, *args, **kwargs):
        return mark_safe(u'<div class="phone_number_field">+7%s</div>' %
                         super(RussianPhoneNumberWidget, self).render(*args, **kwargs))


class RussianPhoneNumberField(forms.MultiValueField):
    widget = RussianPhoneNumberWidget
    default_error_messages = {
        'invalid_local_code': u'Введите правильный телефонный код.',
        'invalid_number': u'Введите правильный телефонный номер.',
    }

    def __init__(self, *args, **kwargs):
        fields = (forms.CharField(max_length=3), forms.CharField(max_length=7))
        super(RussianPhoneNumberField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] in validators.EMPTY_VALUES or len(data_list[0]) != 3 or not data_list[0].isdigit():
                raise ValidationError(self.error_messages['invalid_local_code'])
            if data_list[1] in validators.EMPTY_VALUES or len(data_list[1]) != 7 or not data_list[1].isdigit():
                raise ValidationError(self.error_messages['invalid_number'])
            return '+7' + ''.join(data_list)
        else:
            return None