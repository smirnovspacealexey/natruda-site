from django.core.management.base import BaseCommand
from apps.sber.backend import Sber


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('--------SBER---------')
        sber = Sber()
        print(sber.registrate_order(1, 6))
        # print(sber.check_order_status(2))
        print('---------------------')



