from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from .models import Point, Data


def counter(request):
    template = loader.get_template('customer_interface/counter.html')

    context = {
        'points': Point.objects.all()
    }
    return HttpResponse(template.render(context, request))


def menu_pdf(request):
    current = Data.current()
    print(current.menu.url)
    return HttpResponseRedirect(current.menu.url)

