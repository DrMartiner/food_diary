# -*- coding: utf-8 -*-

from django.db import models
from djangojs.conf import settings


class Food(models.Model):
    name = models.CharField('Наименование', max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name', 'user')
        verbose_name = 'Еда'
        verbose_name_plural = 'Наименование'
        unique_together = ('name', 'user')


class Eating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор')
    pub_date = models.DateTimeField('Время приема', auto_now_add=True)

    @property
    def eatingfoods(self):
        eatingfoods = []
        for eatingfood in EatingFood.objects.filter(eating=self):
            eatingfoods.append({
                'id': eatingfood.pk,
                'name': eatingfood.food.name,
                'count': eatingfood.count,
                'food_id': eatingfood.food.pk,
            })
        return eatingfoods

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Приемы пищи'
        verbose_name_plural = 'Прием пищи'


class EatingFood(models.Model):
    eating = models.ForeignKey(Eating, verbose_name='Прием пищи')
    food = models.ForeignKey(Food, verbose_name='Еда')
    count = models.CharField('Кол-во', max_length=8, blank=True, null=True)