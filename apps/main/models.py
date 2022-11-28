from django.db import models
from django import forms


class Point(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя точки")
    address = models.CharField(max_length=500, verbose_name="Адрес точки")
    volume = models.IntegerField(default=100, verbose_name="рубли")
    picture = models.ImageField(upload_to="img/points", blank=True, null=True, verbose_name="картинка")
    subnetwork = models.CharField(max_length=10, default="")
    ordering = models.IntegerField('ordering', default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('ordering', )


class Data(models.Model):
    menu = models.FileField(upload_to="datas", blank=True, null=True, verbose_name="Меню")
    active = models.BooleanField('active', default=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.active:
            type(self).objects.exclude(pk=self.pk).update(active=False)
        super().save()

    @staticmethod
    def current():
        return Data.objects.filter(active=True).last()

