from django.http import HttpResponse
from django.template import loader
from .models import Signboard


def signboard(request, signboard_slug):
    template = loader.get_template('signboards/signboard.html')

    context = {
        'slug': signboard_slug,
        'signboard': Signboard.objects.filter(slug=signboard_slug, active=True).last(),
    }
    return HttpResponse(template.render(context, request))


def signboards(request):
    template = loader.get_template('signboards/signboards.html')

    context = {
        'signboards': Signboard.objects.filter(active=True),
    }
    return HttpResponse(template.render(context, request))

