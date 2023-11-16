# Generated by Django 3.1.5 on 2023-11-16 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_interface', '0023_menu_minutes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productoption',
            options={'ordering': ['customer_title']},
        ),
        migrations.AlterField(
            model_name='contentoption',
            name='picture',
            field=models.ImageField(blank=True, help_text='картинка товара на сайте для покупателя', null=True, upload_to='img/content_pictures', verbose_name='Иконка'),
        ),
        migrations.AlterField(
            model_name='macroproduct',
            name='picture',
            field=models.ImageField(blank=True, help_text='картинка товара на сайте для покупателя', null=True, upload_to='img/category_pictures', verbose_name='Иконка'),
        ),
        migrations.AlterField(
            model_name='macroproductcontent',
            name='picture',
            field=models.ImageField(blank=True, help_text='картинка товара на сайте для покупателя', null=True, upload_to='img/category_pictures', verbose_name='Иконка'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='icon',
            field=models.ImageField(blank=True, help_text='картинка товара на сайте для покупателя', null=True, upload_to='img/icons', verbose_name='Иконка'),
        ),
    ]
