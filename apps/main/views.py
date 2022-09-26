from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from .models import Point


def counter(request):
    template = loader.get_template('customer_interface/counter.html')

    context = {
        'points': Point.objects.all()
    }
    return HttpResponse(template.render(context, request))
