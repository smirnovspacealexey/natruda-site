# Generated by Django 3.1.5 on 2022-07-06 01:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_interface', '0014_auto_20220706_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='macro_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer_interface.macroproduct', verbose_name='Макротовар'),
        ),
    ]