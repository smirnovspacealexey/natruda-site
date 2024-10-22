from typing import AnyStr
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from slugify import slugify
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.template import loader
from .forms import ConfirmOrderForm, CheckOrderStatus
from .models import MacroProduct, SizeOption, ProductVariant, ProductOption, ContentOption, Menu, MacroProductContent, Order
from apps.main.models import Point
from shawarma_site.settings import SHAW_QUEUE_URL, SEND_ORDER_URL, CHECK_ORDER_STATUS_URL, GET_MENU_URL
from raven.contrib.django.raven_compat.models import client
from urllib.parse import unquote
import sys, traceback
import re
import json
import time
import random
import requests
from django.urls import reverse
from shawarma_site.settings import DEBUG
from apps.yookassa.backend import Yookassa
from apps.sber.backend import Sber

import logging  # del me
logger_debug = logging.getLogger('debug_logger')  # del me


# Create your views here.
def index(request):
    print('index')

    template = loader.get_template('customer_interface/index.html')
    # context = {
    #     'categories': [
    #         {
    #             'customer_title': 'Шаурма',
    #             'items': [
    #                 {
    #                     'id': 1,
    #                     'name': 'Шаурма М',
    #                     'price': 110
    #                 },
    #                 {
    #                     'id': 2,
    #                     'name': 'Шаурма С',
    #                     'price': 150
    #                 },
    #                 {
    #                     'id': 3,
    #                     'name': 'Шаурма Б',
    #                     'price': 210
    #                 },
    #             ]
    #         },
    #         {
    #             'customer_title': 'Напитки',
    #             'items': [
    #                 {
    #                     'id': 4,
    #                     'name': 'Пепси',
    #                     'price': 50
    #                 },
    #                 {
    #                     'id': 5,
    #                     'name': 'Кола',
    #                     'price': 110
    #                 },
    #                 {
    #                     'id': 6,
    #                     'name': 'Фанта',
    #                     'price': 70
    #                 },
    #             ]
    #         }
    #     ]
    # }

    macroproducts = MacroProduct.objects.filter(customer_appropriate=True)
    # context = {
    #     'categories': [
    #         {
    #             'title': category.title,
    #             'customer_title': category.customer_title,
    #             'slug': category.slug,
    #         } for category in macroproducts
    #         ]
    # }
    context = {
        'categories': macroproducts
    }
    # return HttpResponse(template.render(context, request))
    return HttpResponseNotFound("Not Found")


def contacts(request):
    template = loader.get_template('customer_interface/contacts.html')
    return HttpResponse(template.render({}, request))


def about(request):
    template = loader.get_template('customer_interface/about.html')
    return HttpResponse(template.render({}, request))


def menu(request):
    template = loader.get_template('customer_interface/menu.html')
    context = get_menu()
    return HttpResponse(template.render(context, request))


def meat(request, category_slug):
    template = loader.get_template('customer_interface/category_content.html')
    # context = update_menu()
    print(MacroProduct.objects.get(slug=category_slug))
    print(MacroProductContent.objects.filter(macro_product__slug=category_slug))
    context = {
        'category': MacroProduct.objects.get(slug=category_slug),
        'contents': MacroProductContent.objects.filter(macro_product__slug=category_slug, customer_appropriate=True)
    }
    return HttpResponse(template.render(context, request))


def basket(request):
    def get_products_id(order):
        ids = []
        for item in order:
            ids.append(item['id'])

        return ids

    current_order = []
    product_ids = []
    cookies_current_order = request.COOKIES.get('currentOrder', None)
    if cookies_current_order:
        unquoted = unquote(cookies_current_order)
        current_order = json.loads(unquoted)
        product_ids = get_products_id(current_order)

    template = loader.get_template('customer_interface/basket_template.html')
    context = {
        'points': Point.objects.all(),
        'current_order': {
            'products': [

            ]
        }
    }
    print(product_ids)
    print(current_order)
    cooking_time = 15
    logger_debug.info(f'basket current_order: {current_order}')

    for item in current_order:
        product_variant = ProductVariant.objects.filter(menu_item__id=item['id']).first()
        product_options_query = ProductOption.objects.filter(product_variants=product_variant)
        for product_option in product_options_query:
            if product_option.minutes > cooking_time:
                cooking_time = product_option.minutes

        if product_variant and product_variant.minutes > cooking_time:
            cooking_time = product_variant.minutes

        product_options = [
            {
                'obj': product_option,
                'is_enabled': True if product_option.id in get_products_id(item['toppings']) else False,
            } for product_option in product_options_query]
        context['current_order']['products'].append({
            'obj': product_variant,
            'quantity': item['quantity'],
            'product_options': product_options,
        })
    context['cooking_time'] = cooking_time
    logger_debug.info(f'basket: {context}')
    return HttpResponse(template.render(context, request))


def char(request, macroproduct_content_id):
    template = loader.get_template('customer_interface/char_template.html')
    for i in ProductVariant.objects.filter(macro_product_content__id=macroproduct_content_id):
        print(i, i.pk, i.internal_id)
    context = {
        'product': MacroProductContent.objects.get(id=macroproduct_content_id),
        'product_variants': [
            {
                'obj': product_variant,
                'product_options': product_variant.productoption_set.all()
            } for product_variant in ProductVariant.objects.filter(macro_product_content__id=macroproduct_content_id).order_by('size_option__ordering')
        ]
    }
    return HttpResponse(template.render(context, request))


def char_base(request):
    template = loader.get_template('customer_interface/char.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def create_order(request):
    def adjust_ids(original_order_content):
        for order_item in original_order_content:
            menu_item = Menu.objects.get(id=order_item['id'])
            order_item['id'] = menu_item.internal_id
            for topping in order_item['toppings']:
                topping_menu_item = Menu.objects.get(id=topping['id'])
                topping['id'] = topping_menu_item.internal_id
        return json.dumps(original_order_content, ensure_ascii=False)

    template = loader.get_template('customer_interface/create_order.html')
    if request.method == 'POST':
        form = ConfirmOrderForm(request.POST)
        import logging  # del me
        logger_debug = logging.getLogger('debug_logger')  # del me

        if form.is_valid():

            print(request.COOKIES)
            # order_number = ''.join([random.choice('1234567890') for x in range(5)])
            # yk = Yookassa('936939', 'test_NrlH-8JYGRxaDHH0BfoLrh_Z65a1g2e7r4d4BzfgMiY', )
            cleaned_data = form.cleaned_data
            phone_number = clean_phone_number(cleaned_data['phone_number'])
            cleaned_data['phone_number'] = phone_number
            cleaned_data['date'] = cleaned_data['date'].strftime("%d/%m/%Y") if cleaned_data['date'] else None
            cleaned_data['time'] = cleaned_data['time'].strftime("%H:%M:%S") if cleaned_data['time'] else None
            cleaned_data['order_content'] = adjust_ids(json.loads(cleaned_data['order_content']))
            order = Order.objects.create(message=str(request.COOKIES), data=str(cleaned_data))
            # url = yk.create_payment(cleaned_data['total_price'], f'{phone_number}')
            # sber = Sber()
            # res = sber.registrate_order(cleaned_data['total_price'], '00000' + str(order.pk))
            # print(res)

            ##  del
            import ast

            order.save()
            logger_debug.info(f'\n----\n {order}\n{order.data}\n{type(order.data)}')
            data = ast.literal_eval(order.data)
            msg = ast.literal_eval(order.message)
            data.update({'is_paid': True,
                         'is_delivery': True if msg.get('way', '1') == '1' else False,
                         'point': 6})

            logger_debug.info(f'\nsuccessful_payment, data\n {data}\n')
            if cleaned_data['name'] == 'Штильцхен':
                order.paid = True
                order.save()
                response_data = send_order_data(data)
                return HttpResponseRedirect(reverse('successful_payment'))
            else:
                return HttpResponseRedirect(reverse('failed_payment'))

            ## del


            if res[0]:
                url = res[1]['formUrl']
            else:
                url = reverse('failed_payment')

            cleaned_data.update({'url': url})
            if DEBUG:
                return JsonResponse({'success': True, 'url': url})
            return JsonResponse(data=cleaned_data)
        else:
            context = {
                'form': ConfirmOrderForm(request.POST)
            }
            return HttpResponse(template.render(context, request))
    else:
        context = {
            'form': ConfirmOrderForm()
        }
        return HttpResponse(template.render(context, request))


def clean_phone_number(phone_number: AnyStr) -> AnyStr:
    """
    Cleans masked phone number from '-', '(' and ')'.
    :param phone_number: Phone number for processing.
    :return: Cleaned phone number
    """
    cleaned_phone_number = '+' + ''.join(re.findall(r"[0-9]+", phone_number))
    return cleaned_phone_number


def check_order(request):
    template = loader.get_template('customer_interface/check_order.html')
    if request.method == 'POST':
        form = CheckOrderStatus(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            response = check_order_status(clean_phone_number(cleaned_data['phone_number']))
            context = {
                'form': form,
                'order_status': response
            }
            return HttpResponse(template.render(context, request))
        else:
            context = {
                'form': form
            }
            return HttpResponse(template.render(context, request))
    else:
        context = {
            'form': CheckOrderStatus()
        }
        return HttpResponse(template.render(context, request))


def check_order_ajax(request):
    phone_number = request.GET.get('phone_number', None)
    try:
        response = check_order_status(clean_phone_number(phone_number))
    except:
        data = {
            'success': False
        }
        return JsonResponse(data=data)

    data = {
        'success': True,
        'order_status': response
    }
    return JsonResponse(data=data)


def check_order_status(phone_number):
    """
    Requests order status from shawarma server.
    :param phone_number:
    :return:
    """
    response = ""
    if CHECK_ORDER_STATUS_URL != "" and CHECK_ORDER_STATUS_URL is not None:
        result = requests.get(CHECK_ORDER_STATUS_URL, params={'phone_number': phone_number})
        if result.status_code == 200:
            json_results = result.json()
            response = json_results['response']
            return response
        else:
            return 'Ошибка!'
    else:
        responses = ['На модерации', 'Заказу присвоен номер 12', 'Заказ готов!']
        time.sleep(random.random() * 3)
        response = responses[random.randint(0, 2)]
    return response


def send_order_data(order_data):
    # TODO: Implement request
    """
    Sends order data to shawarma server.
    :param order_data:
    :return:
    """
    if SEND_ORDER_URL != "" and SEND_ORDER_URL is not None:
        try:
            result = requests.get(SEND_ORDER_URL, params=order_data)
        except ConnectionError:
            client.captureException()
            return {'success': False, 'msg': 'ConnectionError'}
        except:
            client.captureException()
            return {'success': False, 'msg': 'err'}
        if result.status_code == 200:
            json_results = result.json()
            return json_results
        else:
            return {'success': False, 'msg': f'{result.status_code}'}
    else:
        return {'success': False}


def get_menu():
    """
    Requests menu data from shawarma server.
    :return: Dictionary with menu categories and items.
    """

    if GET_MENU_URL != "" and GET_MENU_URL is not None:
        try:
            result = requests.get(GET_MENU_URL)
        except ConnectionError:
            client.captureException()
            return {
                'categories': []
            }
        except:
            client.captureException()
            return {
                'categories': []
            }
        if result.status_code == 200:
            json_results = result.json()
            response = {
                'categories': json_results['categories']
            }
            return response
        else:
            return {}
    else:
        context = {
            'categories': [
                {
                    'title': 'Шаурма',
                    'items': [
                        {
                            'id': 1,
                            'name': 'Шаурма М',
                            'price': 110
                        },
                        {
                            'id': 2,
                            'name': 'Шаурма С',
                            'price': 150
                        },
                        {
                            'id': 3,
                            'name': 'Шаурма Б',
                            'price': 210
                        },
                    ]
                },
                {
                    'title': 'Напитки',
                    'items': [
                        {
                            'id': 4,
                            'name': 'Пепси',
                            'price': 50
                        },
                        {
                            'id': 5,
                            'name': 'Кола',
                            'price': 110
                        },
                        {
                            'id': 6,
                            'name': 'Фанта',
                            'price': 70
                        },
                    ]
                }
            ]
        }
    return context


def update_menu(request):
    """
    Requests menu data from shawarma server.
    :return: Dictionary with menu categories and items.
    """

    try:
        result = requests.get(GET_MENU_URL)
    except ConnectionError:
        client.captureException()
        return {
            'categories': []
        }
    except:
        client.captureException()
        return {
            'categories': []
        }
    if result.status_code == 200:
        json_results = result.json()
        response = json_results
        print(f'\n\n{len(response["menu_items"])}\n\'')  # del me
        for menu_item in response['menu_items']:
            try:
                local_item = Menu.objects.get(internal_id=menu_item['id'])
                local_item.title = menu_item['name']
                local_item.customer_title = menu_item['name']
                local_item.price = menu_item['price']
                local_item.minutes = menu_item['minutes']
                local_item.save()
            except MultipleObjectsReturned:
                client.captureException()
                print("Failed to update menu item id{} {} because multiple are found!".format(menu_item['id'],
                                                                                              menu_item['name']))
            except ObjectDoesNotExist:
                new_menu_item = Menu(title=menu_item['name'], customer_title=menu_item['name'],
                                     price=menu_item['price'], internal_id=menu_item['id'], minutes=menu_item['minutes'])
                new_menu_item.save()

        for category in response['categories']:
            try:
                local_category = MacroProduct.objects.get(internal_id=category['id'])
                local_category.title = category['title']
                local_category.customer_title = category['customer_title']
                local_category.slug = slugify(category['title'])

                local_category.save()
            except MultipleObjectsReturned:
                client.captureException()
                print("Failed to update category id{} {} because multiple are found!".format(category['id'],
                                                                                             category['title']))
            except ObjectDoesNotExist:
                new_category = MacroProduct(title=category['title'], customer_title=category['customer_title'],
                                            slug=slugify(category['title']),
                                            internal_id=category['id'], customer_appropriate=False)
                new_category.save()

        for content_option in response['content_options']:
            try:
                local_content_option = ContentOption.objects.get(internal_id=content_option['id'])
                local_content_option.title = content_option['title']
                local_content_option.customer_title = content_option['customer_title']
                local_content_option.save()
            except MultipleObjectsReturned:
                client.captureException()
                print("Failed to update category id{} {} because multiple are found!".format(content_option['id'],
                                                                                             content_option['title']))
            except ObjectDoesNotExist:
                new_content_option = ContentOption(title=content_option['title'],
                                                   customer_title=content_option['customer_title'],
                                                   internal_id=content_option['id'])
                new_content_option.save()

        for macro_product_content in response['macro_product_content']:
            try:
                local_mpc_option = MacroProductContent.objects.get(internal_id=macro_product_content['id'])
                local_mpc_option.title = macro_product_content['title']
                local_mpc_option.customer_title = macro_product_content['customer_title']
                local_mpc_option.macro_product = MacroProduct.objects.get(
                    internal_id=macro_product_content['macro_product_id'])
                local_mpc_option.content_option = ContentOption.objects.get(
                    internal_id=macro_product_content['content_option_id'])
                local_mpc_option.save()
            except MultipleObjectsReturned:
                client.captureException()
                print(
                    "Failed to update category id{} {} because multiple are found!".format(macro_product_content['id'],
                                                                                           macro_product_content[
                                                                                               'title']))
            except ObjectDoesNotExist:
                # continue
                try:
                    according_macro = MacroProduct.objects.filter(internal_id=macro_product_content['macro_product_id']).first()
                    according_content = ContentOption.objects.filter(internal_id=macro_product_content['content_option_id']).first()

                    local_mpc_option = MacroProductContent.objects.filter(internal_id=macro_product_content['id']).first()
                    if local_mpc_option:
                        local_mpc_option.title = macro_product_content['title']
                        local_mpc_option.customer_title = macro_product_content['content_option_id']
                        local_mpc_option.internal_id = macro_product_content['customer_title']
                        local_mpc_option.macro_product = macro_product_content['id']
                        local_mpc_option.content_option = according_macro
                        local_mpc_option.customer_appropriate = True
                        local_mpc_option.slug = slugify("{} {}".format(according_macro.customer_title, according_content.customer_title))
                    else:

                        print(ContentOption.objects.filter(internal_id=macro_product_content['content_option_id']))
                        new_mpc_option = MacroProductContent(title=macro_product_content['title'],
                                                             customer_title=macro_product_content['customer_title'],
                                                             internal_id=macro_product_content['id'],
                                                             macro_product=according_macro,
                                                             content_option=according_content,
                                                             customer_appropriate=True,
                                                             slug=slugify("{} {}".format(according_macro.customer_title,
                                                                                         according_content.customer_title)))
                        new_mpc_option.save()
                except:
                    print(f'ERROR: {traceback.format_exc()}')

        for size_option in response['size_options']:
            try:
                local_size_option = SizeOption.objects.get(internal_id=size_option['id'])
                local_size_option.title = size_option['title']
                local_size_option.customer_title = size_option['customer_title']
                local_size_option.save()
            except MultipleObjectsReturned:
                client.captureException()
                print("Failed to update category id{} {} because multiple are found!".format(size_option['id'],
                                                                                             size_option['title']))
            except ObjectDoesNotExist:
                new_size_option = SizeOption(title=size_option['title'],
                                             customer_title=size_option['customer_title'],
                                             internal_id=size_option['id'])
                new_size_option.save()

        for product_option in response['product_options']:
            try:
                local_product_option = ProductOption.objects.get(internal_id=product_option['id'])
                local_product_option.title = product_option['title']
                local_product_option.customer_title = product_option['customer_title']
                local_product_option.menu_item = Menu.objects.get(internal_id=product_option['menu_item_id'])
                local_product_option.save()
            except MultipleObjectsReturned:
                client.captureException()
                print("Failed to update category id{} {} because multiple are found!".format(product_option['id'],
                                                                                             product_option['title']))
            except ObjectDoesNotExist:
                new_product_option = ProductOption(title=product_option['title'],
                                                   customer_title=product_option['customer_title'],
                                                   internal_id=product_option['id'],
                                                   menu_item=Menu.objects.get(internal_id=
                                                                              product_option['menu_item_id']))
                new_product_option.save()

        print(response['product_variants'])
        print('\n\n\n\n\n\n')
        for product_variant in response['product_variants']:
            try:
                print(ProductVariant.objects.filter(internal_id=product_variant['id']))
                local_product_variant = ProductVariant.objects.get(internal_id=product_variant['id'])
                local_product_variant.title = product_variant['title']
                local_product_variant.customer_title = product_variant['customer_title']
                local_product_variant.menu_item = Menu.objects.get(internal_id=product_variant.get('menu_item_id', None))
                local_product_variant.size_option = SizeOption.objects.get(
                    internal_id=product_variant.get('size_option_id', None))
                local_product_variant.content_option = ContentOption.objects.get(
                    internal_id=product_variant.get('content_option_id', None))
                local_product_variant.macro_product = MacroProduct.objects.get(
                    internal_id=product_variant.get('category_id', None))
                print(product_variant.get('macro_product_content_id', None))
                print(MacroProductContent.objects.get(
                    internal_id=product_variant.get('macro_product_content_id', None)))
                local_product_variant.macro_product_content = MacroProductContent.objects.get(
                    internal_id=product_variant.get('macro_product_content_id', None))
                local_product_variant.save()

                local_product_variant__product_options__ids = ProductOption.objects.filter(
                    product_variants=local_product_variant).values_list('internal_id', flat=True)
                new_product_options = set(local_product_variant__product_options__ids).symmetric_difference(
                    set(product_variant['product_options_ids']))
                for local_product_variant__new_product_option in ProductOption.objects.filter(
                        internal_id__in=new_product_options):
                    local_product_variant__new_product_option.product_variants.add(local_product_variant)

            except MultipleObjectsReturned:
                print('MultipleObjectsReturned')
                client.captureException()
                print("Failed to update category id{} {} because multiple are found!".format(product_variant['id'],
                                                                                             product_variant['name'] if 'name' in product_variant else 'noname'))
            except ObjectDoesNotExist:
                print('ObjectDoesNotExist')
                # continue
                menu_item = Menu.objects.get(internal_id=product_variant['menu_item_id'])
                content_option = ContentOption.objects.get(internal_id=product_variant['content_option_id']) if \
                    'content_option_id' in product_variant else None

                size_option = SizeOption.objects.get(internal_id=product_variant['size_option_id']) if \
                    'size_option_id' in product_variant else None

                category = MacroProduct.objects.get(internal_id=product_variant['category_id']) if \
                    'category_id' in product_variant else None

                print(product_variant['macro_product_content_id'])
                macro_product_content = MacroProductContent.objects.filter(internal_id=
                                                                           product_variant['macro_product_content_id']).first() \
                    if 'macro_product_content_id' in product_variant else None

                local_product_variant = ProductVariant.objects.filter(internal_id=product_variant['id']).last()
                if not local_product_variant:
                    new_product_variant = ProductVariant(title=product_variant['title'],
                                                         customer_title=product_variant['customer_title'],
                                                         internal_id=product_variant['id'],
                                                         menu_item=menu_item,
                                                         content_option=content_option,
                                                         size_option=size_option,
                                                         macro_product=category,
                                                         macro_product_content=macro_product_content)
                    new_product_variant.save()
                    for new_product_variant__new_product_option in ProductOption.objects.filter(
                            internal_id__in=product_variant['product_options_ids']):
                        new_product_variant__new_product_option.product_variants.add(new_product_variant)
                else:
                    local_product_variant.title = product_variant['title']
                    local_product_variant.product_variant = product_variant['customer_title']
                    local_product_variant.internal_id = product_variant['id']
                    local_product_variant.menu_item = menu_item
                    local_product_variant.content_option = content_option
                    local_product_variant.size_option = size_option
                    local_product_variant.macro_product = category
                    local_product_variant.macro_product_content = macro_product_content
                    local_product_variant.save()
                    for new_product_variant__new_product_option in ProductOption.objects.filter(
                            internal_id__in=product_variant['product_options_ids']):
                        if local_product_variant not in new_product_variant__new_product_option.product_variants.all():
                            new_product_variant__new_product_option.product_variants.add(local_product_variant)

        if request:
            return HttpResponseRedirect(reverse('admin:customer_interface_menu_changelist'))
        return response
    else:
        if request:
            return HttpResponseRedirect(reverse('admin:customer_interface_menu_changelist'))
        return {}

