# Generated by Django 3.1.5 on 2022-11-28 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_point_subnetwork'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu', models.FileField(blank=True, null=True, upload_to='datas', verbose_name='Меню')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
            ],
        ),
    ]
