# Generated by Django 3.1.5 on 2021-01-24 10:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                (
                'customer_title', models.CharField(default='', max_length=200, verbose_name='Название для покупателя')),
                ('note', models.CharField(max_length=500)),
                ('price', models.FloatField(default=0, validators=[
                    django.core.validators.MinValueValidator(0, "Price can't be negative!")])),
                ('avg_preparation_time', models.DurationField(verbose_name='Average preparation time.')),
                ('guid_1c', models.CharField(default='', max_length=100)),
                ('is_by_weight', models.BooleanField(default=False, verbose_name='На развес')),
                ('customer_appropriate',
                 models.BooleanField(default=False, verbose_name='Подходит для демонстрации покупателю')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='img/icons', verbose_name='Иконка')),
            ],
        ),
    ]
