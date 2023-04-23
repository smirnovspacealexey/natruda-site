from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, resolve
from customer_interface.models import Order
from customer_interface.views import send_order_data
import ast
import requests
import sys, traceback


from .backend import Sber

import logging  # del me
logger_debug = logging.getLogger('debug_logger')  # del me


def test(request):
    template = loader.get_template('customer_interface/test.html')

    context = {
    }
    return HttpResponse(template.render(context, request))


def test1(request):  # del me
    logger_debug.info(f'test1\n {request.GET}\n')


def successful_payment(request):
    context = {}
    if request.GET and 'orderId' in request.GET:
        sber = Sber()
        res = sber.check_order_status(order_id=request.GET['orderId'])
        if res[0] and res[1]['actionCode'] == 0:
            order = Order.objects.filter(pk=res[1]['orderNumber'][5:], paid=False).first()
            order.paid = True
            order.save()
            logger_debug.info(f'\n----\n {order}\n{order.data}\n{type(order.data)}')
            data = ast.literal_eval(order.data)
            msg = ast.literal_eval(order.message)
            data.update({'is_paid': True,
                         'is_delivery': True if msg.get('way', '1') == '1' else False,
                         'point': msg.get('point', None)})

            logger_debug.info(f'\nsuccessful_payment, data\n {data}\n')
            response_data = send_order_data(data)
            logger_debug.info(f'\nsuccessful_payment\n {response_data}\n\n')
            if 'order_number' in response_data:
                order_number = response_data['order_number']
            else:
                order_number = res[1]['orderNumber']
            context.update({'orderNumber': order_number, 'amount': res[1]['amount']/100,
                            'success_in_queue': response_data['success']})
        else:
            return HttpResponseRedirect(reverse('failed_payment'))

    template = loader.get_template('customer_interface/returnUrl.html')
    return HttpResponse(template.render(context, request))


def failed_payment(request):
    template = loader.get_template('customer_interface/failUrl.html')

    context = {
    }
    return HttpResponse(template.render(context, request))


def sber_result(request):
    try:
        logger_debug.info(f'sber_result\n----\n {request.GET}\n{request.GET.get("operation")}')
        logger_debug.info(f"{request.GET.get('operation') == 'deposited' and request.GET.get('status') == '1'}")
        #
        # result = requests.get('http://shawarma.natruda/shaw_queue/send_customers_menu/')
        # logger_debug.info(f'result\n {result}\n')

        if request.GET.get('operation') == 'deposited' and request.GET.get('status') == '1':
            data = {
                "daily_number": request.GET.get('orderNumber'),
                "success": True,
            }

            res = requests.get('http://78.29.36.194/sber/result', params=data)
            logger_debug.info(f'res\n {res}\n')

        return JsonResponse({'success': True})
    except:
        logger_debug.info(f'ERROR: {traceback.format_exc()}')




