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


