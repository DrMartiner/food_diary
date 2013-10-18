# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class SEX:
        MALE = 'M'
        FEEMALE = 'F'
        CHOICES = (
            (MALE, 'Мужской'),
            (FEEMALE, 'Женский'),
        )
    sex = models.CharField('Пол', choices=SEX.CHOICES, max_length=1, default=SEX.MALE)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)

    def __unicode__(self):
        return self.get_full_name()

User._meta.get_field('email')._unique = True