# Generated by Django 3.1.5 on 2021-03-13 08:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('customer_interface', '0009_auto_20210208_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='macroproductcontent',
            name='customer_description',
            field=models.TextField(default='', max_length=312, verbose_name='Описание товара'),
        ),
    ]
