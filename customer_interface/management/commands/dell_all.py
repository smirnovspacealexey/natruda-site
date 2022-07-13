from django.core.management.base import BaseCommand
from customer_interface.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('--------DELL---------')
        print(Menu.objects.all().delete())
        print(MacroProduct.objects.all().delete())
        print(MacroProductContent.objects.all().delete())
        print(SizeOption.objects.all().delete())
        print(ContentOption.objects.all().delete())
        print(ProductVariant.objects.all().delete())
        print(ProductOption.objects.all().delete())
        print('---------------------')



