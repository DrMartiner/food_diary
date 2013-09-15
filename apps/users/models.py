# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager


class UserManager(DjangoUserManager):
    def create_superuser(self, email, password, **extra_fields):
        """ Set email as username, because username can't be blank """
        return super(UserManager, self).create_superuser(email, email, password, **extra_fields)


class User(AbstractUser):
    SEX_MALE = 'M'
    SEX_FEEMALE = 'F'
    SEX_CHOICES = (
        (SEX_MALE, 'Мужской'),
        (SEX_FEEMALE, 'Женский'),
    )
    sex = models.CharField('Пол', choices=SEX_CHOICES, max_length=1, default=SEX_MALE)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return u'%s %s' % (self.last_name, self.first_name)

    @property
    def name(self):
        return '%s %s' % (self.last_name, self.first_name)

User._meta.get_field('email')._unique = True