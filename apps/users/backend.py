# -*- coding: utf-8 -*-

from random import randrange
from django.contrib.sites.models import Site, RequestSite
from registration import signals
from django.contrib.auth import get_user_model, authenticate, login
from registration.backends.default import DefaultBackend
from random_words import RandomWords
from registration.models import RegistrationProfile

User = get_user_model()


def generate_password():
    word = RandomWords().random_word()
    number = randrange(100, 999)
    return '%s-%d' % (word, number)


class RegisterBackend(DefaultBackend):
    def register(self, request, **kwargs):
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        password = generate_password()
        new_user = RegistrationProfile.objects.create_inactive_user(kwargs['phone'], kwargs['email'], password, site)

        new_user.first_name = kwargs['first_name']
        new_user.last_name=kwargs.get('last_name', '')
        new_user.sex=kwargs.get('sex', '')
        new_user.birth_date=kwargs.get('birth_date', '')
        new_user.save()

        # Authenticate the new user
        user = authenticate(username=new_user.username, password=password)
        if user is not None:
            login(request, user)

        # TODO: Send the password

        signals.user_registered.send(sender=self.__class__, user=user, request=request)

        return user