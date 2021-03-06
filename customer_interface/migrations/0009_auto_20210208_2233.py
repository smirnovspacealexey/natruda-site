# Generated by Django 3.1.5 on 2021-02-08 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('customer_interface', '0008_auto_20210208_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='macroproductcontent',
            name='content_option',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE,
                                    to='customer_interface.contentoption', verbose_name='Вариант содержимого'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='macroproductcontent',
            name='macro_product',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE,
                                    to='customer_interface.macroproduct', verbose_name='Макротовар'),
            preserve_default=False,
        ),
    ]
