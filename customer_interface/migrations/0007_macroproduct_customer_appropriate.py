# Generated by Django 3.1.5 on 2021-02-04 17:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('customer_interface', '0006_auto_20210203_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='macroproduct',
            name='customer_appropriate',
            field=models.BooleanField(default=False, verbose_name='Подходит для демонстрации покупателю'),
        ),
    ]
