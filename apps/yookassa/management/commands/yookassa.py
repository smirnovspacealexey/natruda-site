from django.core.management.base import BaseCommand
from apps.yookassa.backend import Yookassa


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('--------YOOKASSA---------')
        yk = Yookassa('870966', 'test_k7g0-DyY5U4lbtDdF2nr7EmwRl7TmsUDwbX7BH9x8O8', )
        yk.create_payment()
        print('---------------------')



