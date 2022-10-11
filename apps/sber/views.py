from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from customer_interface.models import Order
from customer_interface.views import send_order_data
import ast

from .backend import Sber

import logging  # del me
logger_debug = logging.getLogger('debug_logger')  # del me


def test(request):
    template = loader.get_template('customer_interface/test.html')

    context = {
    }
    return HttpResponse(template.render(context, request))


def successful_payment(request):
    context = {}
    if request.GET and 'orderId' in request.GET:
        sber = Sber()
        res = sber.check_order_status(order_id=request.GET['orderId'])
        if res[0] and res[1]['actionCode'] == 0:
            order = Order.objects.filter(pk=res[1]['orderNumber'][5:]).first()
            order.paid = True
            order.save()

            data = ast.literal_eval(order.data)
            data.update({'is_paid': True})
            response_data = send_order_data(data)
            logger_debug.info(f'\nsuccessful_payment\n {response_data}\n\n')
            context.update({'orderNumber': res[1]['orderNumber'], 'amount': res[1]['amount']/100})
        else:
            return HttpResponseRedirect(reverse('failed_payment'))

    template = loader.get_template('customer_interface/returnUrl.html')
    return HttpResponse(template.render(context, request))


def failed_payment(request):
    template = loader.get_template('customer_interface/failUrl.html')

    context = {
    }
    return HttpResponse(template.render(context, request))

