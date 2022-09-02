import requests
import json
from django.urls import reverse, resolve

from shawarma_site.settings import HOST
from .models import SberSettings


class Sber:
    def __init__(self):
        sber_settings = SberSettings.get_active()
        if sber_settings:
            self.login = sber_settings.login
            self.password = sber_settings.password
            self.min_amount = sber_settings.min_amount * 100
            self.max_amount = sber_settings.max_amount * 100
            self.tax_system = sber_settings.tax_system
            if sber_settings.in_test:
                self.host = 'https://3dsec.sberbank.ru/'
            else:
                self.host = 'https://securepayments.sberbank.ru/'
            print(self.login, self.password)
        else:
            raise Exception('need SberSettings active object')

    def registrate_order(self, amount, order_id, ):
        amount = int(amount) * 100
        if amount > self.max_amount:
            return False, f'Сумма заказа больше {self.max_amount/100}'
        if amount < self.min_amount:
            return False, f'Сумма заказа меньше {self.min_amount/100}'

        url = self.host + 'payment/rest/register.do'
        print(HOST + reverse('successful_payment'))
        data = {
            "userName": self.login,
            "password": self.password,
            'amount': amount,
            'orderNumber': order_id,
            'taxSystem': self.tax_system,
            'returnUrl': HOST + reverse('successful_payment'),
            'failUrl': HOST + reverse('failed_payment'),

        }

        print(data)
        res = requests.post(url, data=data)
        if res.status_code == 200:
            response = json.loads(res.content.decode("utf-8"))
            return True, response
        else:
            return False, res.status_code

    def check_order_status(self, order_number=None, order_id=None):
        if not order_number and not order_id:
            return False, 'нужен order_number или order_id'
        url = self.host + 'payment/rest/getOrderStatusExtended.do'
        data = {
            "userName": self.login,
            "password": self.password,
            'orderNumber': order_number,
            'orderId': order_id,

        }
        print(data)
        res = requests.post(url, data=data)
        if res.status_code == 200:
            response = json.loads(res.content.decode("utf-8"))
            return True, response
        else:
            return False, res.status_code

