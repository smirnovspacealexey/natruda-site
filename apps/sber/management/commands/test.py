from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.contrib.sessions.models import Session
import logging
import sys, traceback
import requests

logger_debug = logging.getLogger('debug_logger')


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            res = requests.get('http://78.29.36.194/sber/result?daily_number=881533')
            logger_debug.info(f'res\n {res}\n')
            print(res)

        except:
            logger_debug.info(f'delivery_request ERROR: {traceback.format_exc()}')
            print(traceback.format_exc())


