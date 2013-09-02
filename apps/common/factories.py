# -*- coding: utf-8 -*-

import factory
import datetime
from django.contrib.auth import get_user_model
from apps.food.models import Food
from apps.food.models import Eating
from apps.food.models import EatingFood

User = get_user_model()


class UserF(factory.Factory):
    FACTORY_FOR = User

    email = factory.Sequence(lambda n: 'email{0}@example.com'.format(n))
    username = factory.Sequence(lambda n: 'username{0}'.format(n))


class FoodF(factory.Factory):
    FACTORY_FOR = Food

    name = factory.Sequence(lambda n: 'Food-name{0}'.format(n))
    user = factory.LazyAttribute(lambda a: UserF())


class EatingF(factory.Factory):
    FACTORY_FOR = Eating

    pub_date = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    user = factory.LazyAttribute(lambda a: UserF())


class EatingFoodF(factory.Factory):
    FACTORY_FOR = EatingFood

    eating = factory.LazyAttribute(lambda a: EatingF())
    food = factory.LazyAttribute(lambda a: FoodF())
    count = u'88 шт'