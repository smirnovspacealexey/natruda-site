# Generated by Django 3.1.5 on 2022-10-05 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_interface', '0018_auto_20221003_0707'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
