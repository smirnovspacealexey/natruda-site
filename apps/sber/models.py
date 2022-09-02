from django.db import models
from django import forms


class SberSettings(models.Model):
    TAX_SYSTEMS = [('0', 'общая'),
                   ('1', 'упрощённая, доход'),
                   ('2', 'упрощённая, доход минус расход'),
                   ('3', 'единый налог на вменённый доход'),
                   ('4', 'единый сельскохозяйственный налог'),
                   ('5', 'патентная система налогообложения'), ]

    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    min_amount = models.IntegerField(default=500, verbose_name="минимальная сумма заказа")
    max_amount = models.IntegerField(default=10000, verbose_name="максимальная сумма заказа")
    tax_system = models.CharField(max_length=1, choices=TAX_SYSTEMS)

    in_test = models.BooleanField('тестовый режим', default=False)

    active = models.BooleanField('active', default=True)

    def __str__(self):
        return self.login

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.active:
            type(self).objects.exclude(pk=self.pk).update(active=False)
        super().save()

    @staticmethod
    def get_active():
        return SberSettings.objects.filter(active=True).last()

    class Meta:
        verbose_name = 'Настройки Сбера'
        verbose_name_plural = 'Настройки Сбера'


class SberSettingsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['login', 'password', 'tax_system', 'in_test']
        model = SberSettings
