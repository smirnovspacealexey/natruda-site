from django.core.management.base import BaseCommand
from customer_interface.models import *
import requests


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('--------ToQueue---------')

        # url = 'http://127.0.0.1:8001/shaw_queue/order-from-site/'
        url = 'http://shawarma.natruda/shaw_queue/order-from-site/'
        data = {'content': [{'id': 17, 'title': 'Соус Белый', 'price': 50, 'quantity': 1, 'note': 'НЕ ГОТОВИТЬ. ТЕСТОВЫЙ ЗАКАЗ!!!!!'}],
                'delivery': True,
                'point': '24'}

        res = requests.post(url, json=data)
        print(res)
        print('---------------------')



