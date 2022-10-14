# Generated by Django 3.1.5 on 2022-10-14 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_interface', '0020_order_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='macroproduct',
            name='customer_appropriate',
            field=models.BooleanField(default=False, verbose_name='Показывать'),
        ),
        migrations.AlterField(
            model_name='macroproductcontent',
            name='customer_appropriate',
            field=models.BooleanField(default=False, verbose_name='Показывать'),
        ),
        migrations.AlterField(
            model_name='macroproductcontent',
            name='customer_description',
            field=models.TextField(blank=True, default='', max_length=312, null=True, verbose_name='Описание товара'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='customer_appropriate',
            field=models.BooleanField(default=False, verbose_name='Показывать'),
        ),
    ]