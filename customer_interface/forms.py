from typing import List, Tuple

from django import forms


class ConfirmOrderForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'required': True,
        'placeholder': 'Введите имя',
        'pattern': r"^[А-Яа-яЁёA-Za-z\s]+$",  # '+7[0-9]{10}',
        'title': 'Имя не может содержать цифр и спец. знаков.',
        'class': 'form-control'
    }), help_text='Имя не может содержать цифр и спец. знаков.', label='Ваше имя', max_length=12)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'required': True,
        'placeholder': '+7(XXX)-XXX-XX-XX',
        'pattern': r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$",  # r"\+7[0-9]{10}",  # '+7[0-9]{10}',
        'title': 'Введите номер в формате +7(XXX)-XXX-XX-XX',
        'type': 'tel',
        'class': 'form-control'
    }), help_text='Введите номер в формате +7(XXX)-XXX-XX-XX', label='Ваш номер телефона')
    comment = forms.CharField(max_length=100, label="Комментарий", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'title': ''
    }), required=False)
    order_content = forms.CharField(widget=forms.HiddenInput(attrs={'required': True}))
    deliver_to_time_CHOICES = [('nearest_time', 'Ближайшее время'),
                               ('exact_time', 'Точное время')]
    deliver_to_time = forms.ChoiceField(choices=deliver_to_time_CHOICES, widget=forms.RadioSelect)
    delivery_CHOICES = [('false', 'Самовывоз'),
                        ('true', 'Доставка')]
    is_delivery = forms.ChoiceField(choices=delivery_CHOICES, widget=forms.RadioSelect)
    date = forms.DateField(required=False)
    time = forms.TimeField(required=False)
    address = forms.CharField(required=False)
    delivery_place_CHOICES = [('1', 'Точка 1'),
                              ('2', 'Точка 2'),
                              ('3', 'Точка 3')]
    delivery_place = forms.ChoiceField(choices=delivery_place_CHOICES, widget=forms.Select, required=False)
    CASH_PAYMENT = "CSH"
    CASHLESS_PAYMENT = "CLS"
    MIXED_PAYMENT = "MXD"
    PAYMENT_CHOICES = [
        (CASH_PAYMENT, 'Наличные'),
        (CASHLESS_PAYMENT, 'Безнал'),
        (MIXED_PAYMENT, 'Смешанная')]
    payment = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect, required=False)
    cash_pay = forms.CharField(widget=forms.TextInput(attrs={
        'pattern': '[0-9]',
    }), required=False)
    total_price = forms.CharField(required=True)


class CheckOrderStatus(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'required': True,
        'placeholder': '+7(XXX)-XXX-XX-XX',
        'pattern': r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$",  # r"\+7[0-9]{10}",  # '+7[0-9]{10}',
        'title': 'Введите номер в формате +7(XXX)-XXX-XX-XX',
        'type': 'tel',
        'class': 'form-control'
    }), help_text='Введите номер в формате +7(XXX)-XXX-XX-XX', label='Ваш номер телефона')
