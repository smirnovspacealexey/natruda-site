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
            if args:
                daily_number = args[0]
            else:
                daily_number = '384026'

            res = requests.get(f'http://78.29.36.194/sber/result?daily_number={daily_number}')
            logger_debug.info(f'res\n {res}\n')
            print(res)

        except:
            logger_debug.info(f'delivery_request ERROR: {traceback.format_exc()}')
            print(traceback.format_exc())


