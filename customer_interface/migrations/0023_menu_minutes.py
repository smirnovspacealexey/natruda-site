# Generated by Django 3.1.5 on 2022-11-23 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_interface', '0022_auto_20221014_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='minutes',
            field=models.IntegerField(default=15, verbose_name='время готовки в минутах'),
        ),
    ]
