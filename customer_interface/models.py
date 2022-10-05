from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db import models
import datetime


# Create your models here.


class Menu(models.Model):
    title = models.CharField(max_length=200)
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    price = models.FloatField(default=0, validators=[MinValueValidator(0, "Price can't be negative!")])
    guid_1c = models.CharField(max_length=100, default="")
    internal_id = models.IntegerField(default=-1, verbose_name="ID из внутренней базы")
    weight = models.IntegerField(verbose_name="Вес товара", blank=True, null=True)
    meat_weight = models.IntegerField(verbose_name="Вес мяса в товаре", blank=True, null=True)
    # category = models.ForeignKey(MenuCategory, on_delete=models.SET_NULL, null=True)
    is_by_weight = models.BooleanField(verbose_name="На развес", default=False)
    note = models.TextField(verbose_name="Описание", blank=True, null=True)
    customer_appropriate = models.BooleanField(verbose_name="Подходит для демонстрации покупателю", default=False)
    icon = models.ImageField(upload_to="img/icons", blank=True, null=True, verbose_name="Иконка")

    def __str__(self):
        return u"{}".format(self.title) if self.title else f'Noname id:{self.internal_id}'


class MacroProduct(models.Model):
    """
    Шаурма, Бурум, Холодные напитки...
    """
    title = models.CharField(max_length=200)
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    slug = models.SlugField(unique=True, default='')
    picture = models.ImageField(upload_to="img/category_pictures", blank=True, null=True, verbose_name="Иконка")
    internal_id = models.IntegerField(default=-1, verbose_name="ID из внутренней базы")
    customer_appropriate = models.BooleanField(verbose_name="Подходит для демонстрации покупателю", default=False)
    ordering = models.IntegerField('ordering', default=0)

    def __str__(self):
        return u"{}".format(self.title) if bool(self.picture) else u"{} [No Photo]".format(self.title)

    class Meta:
        ordering = ('ordering', )


class SizeOption(models.Model):
    """
    Большая, Средняя, 0.33л, 0.5л...
    """
    title = models.CharField(max_length=200)
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    internal_id = models.IntegerField(default=-1, verbose_name="ID из внутренней базы")

    def __str__(self):
        return u"{}".format(self.title)


class ContentOption(models.Model):
    """
    Курица, Свинина, Чай, Кола...
    """
    title = models.CharField(max_length=200)
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    picture = models.ImageField(upload_to="img/content_pictures", blank=True, null=True, verbose_name="Иконка")
    internal_id = models.IntegerField(default=-1, verbose_name="ID из внутренней базы")

    def __str__(self):
        return u"{}".format(self.title) if bool(self.picture) else u"{} [No Photo]".format(self.title)


class MacroProductContent(models.Model):
    """
    Шаурма со свининой, Говяжий шашлык, Coca-cola...
    """
    title = models.CharField(max_length=200)
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    customer_description = models.TextField(max_length=312, default="", verbose_name="Описание товара")
    slug = models.SlugField(unique=True, default='')
    picture = models.ImageField(upload_to="img/category_pictures", blank=True, null=True, verbose_name="Иконка")
    customer_appropriate = models.BooleanField(verbose_name="Подходит для демонстрации покупателю", default=False)
    content_option = models.ForeignKey(ContentOption, on_delete=models.CASCADE, verbose_name="Вариант содержимого")
    macro_product = models.ForeignKey(MacroProduct, related_name='contents', on_delete=models.CASCADE, verbose_name="Макротовар")
    internal_id = models.IntegerField(default=-1, verbose_name="ID из внутренней базы")

    def __str__(self):
        return u"{}".format(self.title) if bool(self.picture) else u"{} [No Photo]".format(self.title)


class ProductVariant(models.Model):
    """
    Should be used to link different contents and sizes of products of one type. (Большая Куриная Шаурма, 0.33л Кола)
    """
    title = models.CharField(max_length=200)
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="Товар из меню 1С")
    size_option = models.ForeignKey(SizeOption, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Вариант размера")
    content_option = models.ForeignKey(ContentOption, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Вариант содержимого")
    macro_product = models.ForeignKey(MacroProduct, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Макротовар")
    macro_product_content = models.ForeignKey(MacroProductContent, on_delete=models.CASCADE,
                                              verbose_name="Содержимое макротовара", null=True)
    internal_id = models.IntegerField(default=-1, verbose_name="ID из внутренней базы")

    def __str__(self):
        return u"{}".format(self.title)


class ProductOption(models.Model):
    """
    Should be used to link toppings menu_items, such as cheese, onion rings, sugar, etc. with product_variants
    """
    title = models.CharField(max_length=200)
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="Товар из меню 1С")
    product_variants = models.ManyToManyField(ProductVariant, verbose_name="Вариант товара")
    internal_id = models.IntegerField(default=-1, verbose_name="ID из внутренней базы")

    def __str__(self):
        return u"{}".format(self.title)


class Order(models.Model):
    message = models.TextField(verbose_name='message')
    paid = models.BooleanField(verbose_name="оплачено", default=False)
    date = models.DateTimeField('дата, время', default=timezone.now)

    def __str__(self):
        return str(self.pk)
