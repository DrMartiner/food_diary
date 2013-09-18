# -*- coding: utf-8 -*-

from random import randrange
from registration import signals
from django.contrib.auth import get_user_model, authenticate, login
from registration.backends.default import DefaultBackend
from random_words import RandomWords

User = get_user_model()


def generate_password():
    word = RandomWords().random_word()
    number = randrange(100, 999)
    return '%s-%d' % (word, number)


class RegisterBackend(DefaultBackend):
    def register(self, request, **kwargs):
        # Save new user
        user = User(
            email=kwargs['email'],
            username=kwargs['phone'],
            first_name=kwargs['first_name'],
            last_name=kwargs.get('last_name', ''),
            sex=kwargs.get('sex', ''),
            birth_date=kwargs.get('birth_date', ''),
        )
        user.save()

        password = generate_password()
        user.set_password(password)

        # TODO: Send the password

        # Authenticate the new user
        user = authenticate(username=user.username, password=password)
        if user is not None:
            login(request, user)

        signals.user_registered.send(sender=self.__class__, user=user, request=request)
        return user