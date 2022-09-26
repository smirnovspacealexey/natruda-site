from django.db import models
from django import forms


class Point(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя точки")
    address = models.CharField(max_length=500, verbose_name="Адрес точки")
    volume = models.IntegerField(default=100, verbose_name="рубли")
    ordering = models.IntegerField('ordering', default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('ordering', )

