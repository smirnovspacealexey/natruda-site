from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from .models import Point, Data
from shawarma_site.settings import HOST


def counter(request):
    template = loader.get_template('customer_interface/counter.html')

    context = {
        'points': Point.objects.all()
    }
    return HttpResponse(template.render(context, request))


def menu_pdf(request):
    current = Data.current()
    template = loader.get_template('customer_interface/pdf.html')
    context = {
        'url': HOST[:-1] + current.menu.url,
        'title': 'меню'
    }
    return HttpResponse(template.render(context, request))


def menu_pictures(request):
    current = Data.current()
    template = loader.get_template('customer_interface/pictures-new.html')
    mobile = request.user_agent.is_mobile
    HOST = 'http://127.0.0.1:8000/'
    context = {
        'HOST': HOST[:-1],
        'pictures': current.menu_pictures.filter(mobile=mobile).order_by('ordering'),
        'title': 'меню',
        'mobile': mobile,
        'picture': current.menu_pictures.first()
    }
    return HttpResponse(template.render(context, request))


